# Copyright 2020 TWO SIGMA OPEN SOURCE, LLC  #
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from queue import Empty
from jupyter_client.manager import KernelManager
import json


class JVMKernelMagic:

    def __init__(self, kernel_name, context):
        self.km = None
        self.kc = None
        self.comms = []
        self.kernel_name = kernel_name
        self.context = context
        self.start()

    def start(self):
        self.km = KernelManager()
        self.km.kernel_name = self.kernel_name
        self.km.start_kernel(extra_arguments=[self.context])
        self.kc = self.km.client()
        self.kc.start_channels()
        self.kc.wait_for_ready()

    def stop_kernel(self):
        self.kc.stop_channels()
        self.km.shutdown_kernel(now=True)

    def run_cell(self, code):
        if not self.km:
            self.start()
        self.kc.execute(code, allow_stdin=True)

    def get_shell_msg(self):
        return self.kc.get_shell_msg()

    def get_iopub_msg(self):
        try:
            msg = self.kc.get_iopub_msg(timeout=1)
            return msg
        except Empty:
            return None

    def pass_msg(self, msg_raw):
        msg_json = json.loads(msg_raw)
        content = msg_json['content']
        msg_type = msg_json['header']['msg_type']
        msg = self.kc.session.msg(msg_type, content)
        self.kc.shell_channel.send(msg)
        return None
