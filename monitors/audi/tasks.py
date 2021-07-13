from __future__ import absolute_import
from celery import shared_task

import time
import sys
from os import path
import logging as logger
import requests
# 注意：这是celery的bug, 如果直接像下面写，则会提示找不到task
# import audi_config
from . import audi_config as config

FORMAT = '%(asctime)s %(filename)s %(funcName)s %(lineno)d %(message)s'
logger.basicConfig(level=logger.DEBUG, format=FORMAT)

class CheckProxyService(object):
    """
    定时验证proxy 服务以及后端识别服务
    """
    audio_path = config.AUDI_AUDIO_FILE
    path = config.AUDI_CHECK_PATH
    status_path = config.DEFAULT_STATUS
    hosts = config.AUDI_SERVER_URLS

    def __init__(self, config=None):
        """
        初始化session 以及准备测试音频
        """
        super().__init__()
        self.sess = requests.Session()
        self.audio_data = self.get_audiodata(self.audio_path, random=True)

    @staticmethod
    def get_audiodata(path, chunk_size=1000000, random=False, number=1):
        logger.debug("Read Audio file: {}".format(path))
        with open(path, 'rb') as f:
            audio_data = f.read();
        # Split audio data 
        audio_chunks = []
        for i in range(0, len(audio_data), chunk_size):
            audio_chunks.append(audio_data[i*chunk_size:(i+1)*chunk_size])
        return audio_chunks

    def evaluate_status(self, hosts=hosts):
        assert len(hosts) >= 1
        for host in hosts:
            status_url = ''.join(["https://", host, self.status_path])
            logger.debug("host: {}, status url: {}".format(host, status_url))

            resp = self.sess.get(status_url)
            if resp.status_code != requests.codes.ok:
                logger.error("url: {} status response code: {}".format(status_url,
                                                                       resp.status_code))

        return True

    def evaluate(self, hosts=hosts):
        result = self.evaluate_status(hosts)
        assert result == True
        for host in hosts:
            service_url = ''.join(["https://", host, self.path])
            logger.info("service url: {}".format(service_url))
            # Use default wave format audio file as client data, split it.
            service_result = self.send_audio_with_header(service_url, self.audio_data)
            logger.debug("email host user: {}".format(config.EMAIL_HOST_USER))
#            if True:
#                send_mail('Audi proxy service failed',
#                          '',
#                          config.EMAIL_HOST_USER,
#                          config.EMAIL_TO_USER)

        return True

    def send_audio_with_header(self, url, post_data, default_headers=config.AUDI_HEADERS):
        headers = default_headers
        logger.info("post data length: {}".format(len(post_data)))
        for i in range(1, len(post_data)+1):
            if i == 1:
                output_header = headers
                output_header['part_id'] = str(i)
            else:
                output_header['msg_id'] = headers['msg_id']
                output_header['part_id'] = str(i)
            if (i+1 == len(post_data)+1) or (len(post_data) == 1):
                output_header["last_id"] = "true"
                logger.debug("last data, set last_id=true")
            resp = self.__send_data(url, post_data[i-1], output_header)
            if resp.status_code != requests.codes.ok:
                logger.error("Send audio failed: status_code: {},"
                             "reponse: {}".format(resp.status_code, resp.text))
        return True

    def __send_data(self, url, data, headers):
        server_url = ''.join([url, "?msg_id=", headers['msg_id']])
        logger.debug("url: {}, header: {}".format(server_url, headers))
        resp = requests.post(server_url, headers=headers, data=data)
        logger.info("response: dm state: {}".format(resp.headers["dm_state"]))
        logger.info("response body: {}".format(resp.text))
        return resp


@shared_task
def CheckAudiVoice(msg=None):
    logger.info("Evaluate audi service")
    if msg is not None:
        logger.info("msg: {}".format(msg))
    CheckProxyService().evaluate()
    return True


if __name__ == "__main__":
    CheckProxyService().evaluate()
