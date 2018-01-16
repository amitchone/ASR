echo Installing requirements for MFCC/DTW feature extraction...
echo
cd ..
virtualenv venv
. venv/bin/activate
brew install portaudio 
pip install -r install/requirements.txt
echo
echo Installation complete!
