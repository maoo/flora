# Flora

Flora is a virtual plan assistant, originally designed to help kids to take care of their first plants.

Flora is composed by:

1. a poller, `poller.py`, that uses Mi Flora to pull data from a (Mi Plant) sensor installed in the plant soil and PlantCV to analyise the pictures taken
2. a web application that runs on http://raspberrypi.local:3000 and shows the flora animated cartoon, the sensor levels (temperature, light, moisture, humidity) and notifications (thirsty, hungry, cold, warm, missing light, too much light)

## Run locally

1. Build the project, using `npm install`
2. Create a data stream:
```
touch data/flora.csv
echo "21:52:27-18-Sep-19,25.2,63,126,1,57,500,83,98" >> data/flora.csv
```
3. Run the poller, with `npm run poller`
4. Run the app, with `npm start`
5. `open http://raspberrypi.local:3000`
6. Monitor the poller and nodeJS output, to check if data is flowing, using `tail -f data/flora.csv`

## Preparing a Raspberry PI

This installation is based on [Raspbian Buster](https://www.raspberrypi.org/blog/buster-the-new-version-of-raspbian/); when inside, run the following configuration steps:
```
sudo su
apt-get update -y
apt-get upgrade -y
apt-get autoremove -y
apt-get clean -y
apt-get install -y nodejs npm
```

Now we need to use [berryconda](https://github.com/jjhelmus/berryconda) (armv6l archicture), in order to install PlantCV; miflora and picamera will be normally installed with `pip`
```
wget -O install-berryconda.sh "https://github-production-release-asset-2e65be.s3.amazonaws.com/75886189/cee3b8a8-5fd0-11e7-9c4d-49e02b8d9630?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20190827%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20190827T190041Z&X-Amz-Expires=300&X-Amz-Signature=fc61660a227a9486ba0fe81806b6319957844a139c4b6f950c69c95a07505433&X-Amz-SignedHeaders=host&actor_id=327285&response-content-disposition=attachment%3B%20filename%3DBerryconda3-2.0.0-Linux-armv6l.sh&response-content-type=application%2Foctet-stream"
chmod +x install-berryconda.sh && ./install-berryconda.sh -b
/root/berryconda3/bin/conda install plantcv
cd /root/berryconda3/bin
./pip install miflora picamera
```

## Deploying to a Raspberry PI

Simply run `npm run build ; npm run deploy`; default SSH password is `raspberry`.
