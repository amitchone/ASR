echo Installing required packages for MFCC/DTW feature extraction...
echo
brew install portaudio
pip install virtualenv
cd ..
virtualenv venv
. venv/bin/activate
pip install -r install/requirements.txt
sudo ln -s /usr/local/mysql/lib/libmysqlclient.18.dylib /usr/local/lib/libmysqlclient.18.dylib
echo
echo Installation complete!
