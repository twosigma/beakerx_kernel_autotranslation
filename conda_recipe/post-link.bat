@echo off
(
  REM Uninstall BeakerX notebook extension
  "%PREFIX%\Scripts\beakerx_kernel_autotranslation.exe" "install"
) >>"%PREFIX%\.messages.txt" 2>&1