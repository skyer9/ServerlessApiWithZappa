# Serverless API with Zappa

[여기](https://hidekuma.github.io/serverless/aws/lambda/apigateway/zappa/python-zappa/) 에 있는 강좌를 기반으로 Zappa 개발환경을 구성합니다.

## Install Zappa

Python 3.X 를 설치합니다.

```bash
python -V
sudo yum list | grep python3
sudo yum install python36
python3 -V
```

Virtualenv 를 설치합니다.

```bash
sudo pip-3.6 install virtualenv virtualenvwrapper
```

가상환경은 아래의 명령으로 생성할 수 있습니다.

```bash
# create
virtualenv --python=python3.6 <가상환경이름>
# activate
source <가상환경이름>/bin/activate
# deactivate
deactivate
```

## Start Zappa Application

Zappa 플러그인을 설치합니다.

```bash
virtualenv --python=python3.6 zappa-test
source zappa-test/bin/activate
pip install zappa
pip install flask
zappa init
```

```bash
What do you want to call this environment (default 'dev'):
What do you want to call your bucket? (default 'zappa-vpm0iz6s0'):
Where is your app's function?: app.app
Would you like to deploy this application globally? (default 'n') [y/n/(p)rimary]: n
Does this look okay? (default 'y') [y/n]:
```

## Run app([app.py](app.py))

로컬에서 앱을 실행합니다.

```bash
python app.py test
```

```bash
curl http://localhost:4000/
```

AWS 에 앱을 설치하려면 아래 명령을 실행합니다.

```bash
aws configure
zappa deploy dev
```

```bash
curl https://x7qm6eeb9b.execute-api.ap-northeast-2.amazonaws.com/dev
```

설치된 앱을 제거하려면 아래 명령을 실행합니다.

```bash
zappa undeploy dev
```

## Running with CloudFront([cf_with_custom_domain.py](templates/cf_with_custom_domain.py))

캐싱과 커스텀 도메인 연동을 위해 CloudFront 을 이용합니다.

```bash
python cfn.py -c -t cf_with_custom_domain
```
