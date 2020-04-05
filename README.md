# COVID-19 bot

This bot will periodically post the most up-to-date data regarding the COVID-19 pandemic. We will use [this](https://corona.lmao.ninja/) API, initially. This API uses data from:

- Worldometer (which in turn is pulling from the Chinese National Health Comission and other myriad sources) 
- Johns Hopkins University CSSE [repo here](https://github.com/CSSEGISandData/COVID-19)
- Wikipedia [article here](https://en.wikipedia.org/wiki/COVID-19_testing) 

Visit us at twitter.com/COVID_19bot!

## Architecture

This application will be deployed as an HTTP-triggered Cloud Function on Google Cloud Platform, and triggered by Cloud Scheduler. It's a `Python 3.7` app. Dependency management is handled by `pipenv`, code formatting by `black`, linting and type checking by `mypy`.
