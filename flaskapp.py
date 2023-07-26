import boto3
from boto3.dynamodb.conditions import Attr, Key
from flask import Flask, render_template, request, redirect, url_for, session
from botocore.exceptions import ClientError

#Create instance of flask
app = Flask(__name__)
#Using boto3 to access DynamoDB
dynamodb = boto3.resource('dynamodb', region_name = 'us-east-1')
s3 = boto3.client('s3')

app.secret_key = '9876543210'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        table = dynamodb.Table('Login')
        response = table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        items = response.get('Items')
        if len(items) > 0 and items[0]['password'] == pwd:
            user_name = items[0]['user_name']
            session['email'] = email
            return render_template('mainpage.html', user_name=user_name)
            
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error, email=email)
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        user_name = request.form['user_name']
        pwd = request.form['password']
        table = dynamodb.Table('Login')
        response = table.get_item(
            Key={
                'email': email,
                'user_name': user_name
            }
        )
        if 'Item' in response:
            error = "The email already exists"
            return render_template('register.html', error=error)
        else:
            table.put_item(
                Item={
                    'email': email,
                    'user_name': user_name,
                    'password': pwd
                }
            )
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':
        table = dynamodb.Table('Login')
        response = table.query(
            KeyConditionExpression=Key('email').eq(session['email'])
        )
        item = response['Items'][0]
        user_name = item['user_name']
        if 'query' in request.form:
            title = request.form['title']
            year = request.form['year']
            artist = request.form['artist']
            music_table = dynamodb.Table('music3')
            
            filter_expression = None

            if title:
                filter_expression = Attr('title').eq(title)

            if year:
                year_condition = Attr('year').eq(int(year))
                filter_expression = year_condition if filter_expression is None else filter_expression & year_condition

            if artist:
                artist_condition = Attr('artist').eq(artist)
                filter_expression = artist_condition if filter_expression is None else filter_expression & artist_condition

            if filter_expression is None:
                error = "Please provide at least one search parameter"
                return render_template('mainpage.html', error=error)

            query_response = music_table.scan(FilterExpression=filter_expression)
            print(query_response)
            items = query_response['Items']
            if not items:
                error = "No result is retrieved. Please query again"
                return render_template('mainpage.html', error=error)
            else:
                user_name = item['user_name']
                return render_template('mainpage.html', user_name=user_name, items=items)
            
        elif 'subscribe' in request.form:
            title = request.form['title']
            year = request.form['year']
            artist = request.form['artist']
            music_table = dynamodb.Table('music')
            subscribe_response = music_table.scan(
                FilterExpression=Attr('title').contains(title) & 
                Attr('year').eq(year) & Attr('artist').contains(artist)
            )
            item = subscribe_response['Items'][0]
            music_id = item['music_id']
            s3.Bucket('music-images').put_object(
                Key=str(music_id) + '.jpg',
                Body=item['image']
            )
            subscription_table = dynamodb.Table('subscription')
            subscription_table.put_item(
                Item={
                    'email': session['email'],
                    'music_id': music_id
                }
            )
            return redirect(url_for('main'))
        elif 'remove' in request.form:
            music_id = request.form['music_id']
            subscription_table = dynamodb.Table('subscription')
            subscription_table.delete_item(
                Key={
                    'email': session['email'],
                    'music_id': music_id
                }
            )
            s3.Bucket('music-images').delete_objects(
                Delete={
                    'Objects': [
                        {
                            'Key': str(music_id) + '.jpg'
                        }
                    ]
                }
            )
            return redirect(url_for('main'))
    subscription_table = dynamodb.Table('subscription')
    subscription_response = subscription_table.scan(
        FilterExpression=Attr('email').eq(session['email'])
    )
    items = subscription_response['Items']
    return render_template('mainpage.html', username=user_name, items=items)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)