echo Installing required packages for MFCC/DTW feature extraction...
echo
cd ..
virtualenv venv
. venv/bin/activate
brew install portaudio
pip install -r install/requirements.txt
sudo ln -s /usr/local/mysql/lib/libmysqlclient.18.dylib /usr/local/lib/libmysqlclient.18.dylib
echo
echo Installation complete!
