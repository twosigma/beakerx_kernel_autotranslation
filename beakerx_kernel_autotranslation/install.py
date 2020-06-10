# Copyright 2017 TWO SIGMA OPEN SOURCE, LLC
#
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

'''Installs BeakerX into a Jupyter and Python environment.'''

import subprocess


def _uninstall_serverextension():
    subprocess.check_call(
        ["jupyter", "serverextension", "disable", "beakerx_kernel_autotranslation", "--py", "--sys-prefix"])


def _install_serverextension():
    subprocess.check_call(
        ["jupyter", "serverextension", "enable", "beakerx_kernel_autotranslation", "--py", "--sys-prefix"])


def install(args):
    _install_serverextension()


def uninstall(args):
    _uninstall_serverextension()


if __name__ == "__main__":
    install()
