# kivy-chat
Simple Chat app using KivyMD and Pusher.com

Cannot run on iOS because of the PyNaCl / nacl package Pusher module uses.
specifically the _sodium.abi13.so module

Possiblie Solution:
https://github.com/pyca/pynacl/blob/master/src/libsodium/dist-build/ios.sh
