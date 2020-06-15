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

from py4j.clientserver import ClientServer, JavaParameters, PythonParameters
from jupyter_client.kernelspec import NoSuchKernel
import json
import sys
from .jvm_kernel_magic import JVMKernelMagic

class PythonEntryPoint(object):

    def __init__(self, kernel_name, context):
        self.pm = JVMKernelMagic(kernel_name, context)

    def evaluate(self, code):
        print('code for evaluate {}'.format(code))
        self.pm.run_cell(code)
        return None

    def getShellMsg(self):
        shellMsg = self.pm.get_shell_msg()
        return json.dumps(shellMsg, default=str)

    def getIopubMsg(self):
        iopubMsg = self.pm.get_iopub_msg()
        return json.dumps(iopubMsg, default=str)

    def shutdownKernel(self):
        self.pm.stop_kernel()
        return None

    def sendMessage(self, msg_raw):
        self.pm.pass_msg(msg_raw)
        return None

    class Java:
        implements = ["com.twosigma.beakerx.kernel.PythonEntryPoint"]


class Py4JServer:
    def __init__(self, port, pyport, kernel_name, context):
        try:
            pep = PythonEntryPoint(kernel_name, context)
        except NoSuchKernel:
            sys.exit(2)
        ClientServer(
            java_parameters=JavaParameters(port=int(port)),
            python_parameters=PythonParameters(port=int(pyport)),
            python_server_entry_point=pep)
        print('Py4j server is running')


if __name__ == '__main__':
    Py4JServer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
