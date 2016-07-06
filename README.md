# IlliniGuide
A course and professor guide for [UIUC](https://uiuc.edu). Built in Python, Flask, and PostgreSQL.

*Note: Any questions, comments, feedback or feature requests should be directed to [xasos](http://github.com/xasos) or via an [issue](https://github.com/xasos/Coins/issues) in this repo.*

## Development

```sh
$ git clone https://github.com/xasos/IlliniGuide.git
$ cd IlliniGuide
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python run.py
```

## Deploy to Heroku
```sh
$ heroku create --stack cedar
$ heroku addons:add shared-database
$ git push heroku master
```

## Contributing
[Contributing Guidelines](CONTRIBUTING.md)

## License
[MIT License](LICENSE)
