echo Installing requirements for MFCC/DTW feature extraction...
echo
cd ..
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
echo
echo Installation complete!
