from flask import Flask,render_template
import pygal
import psycopg2

app = Flask(__name__)


@app.route('/<name>')
def hello_world(name):
    return '<hi> Hello {} </hi>!'.format(name)
#return f"this is (name)"

@app.route('/person/<name>/<int:age>')
def person(name, age):
    return'<h1> {} is {} years old </h1>'.format(name,age)

@app.route('/numbers/<int:n1>/<int:n2>')
def numbers (n1,n2):
    total =n1+n2
    return str(total)

@app.route('/home')
def templating():



    data=[('IE',19.5),
          ('Firefox', 36.6),
          ('Chrome', 36.3),
          ('Safari', 4.5),
          ('Opera', 2.3)
          ]
    # for i in data:
    pie_chart =pygal.Pie()
    pie_chart.title='Browser usage in February 2012 (in %)'
    pie_chart.add(data[0][0],data[0][1])
    pie_chart.add(data[1][0],data[1][1])
    pie_chart.add(data[2][0],data[2][1])
    pie_chart.add(data[3][0],data[3][1])
    pie_chart.add(data[4][0],data[4][1])

    pie_data = pie_chart.render_data_uri()

    data_line = [('janauary', 20),
                 ('febuary', 40),
                 ('march', 31),
                 ('april', 82),
                 ('may', 40),
                 ('june', 50),
                 ('july', 87),
                 ('august', 40)
                 ]

    coon = psycopg2.connect("dbname = 'postgres' user ='postgres' host ='localhost' password =33200161")
    cursor = coon.cursor()
    cursor.execute("""SELECT EXTRACT (MONTH FROM sales.created_at) AS months , SUM (sales.quantity) as "TOTAL SALES"
    FROM public.sales
    GROUP BY months
    ORDER BY months""")


    records = cursor.fetchall()



    x = []
    sales = []
    for i in records:
        x.append(i[0])
        sales.append(i[1])
    print(x)
    print(sales)
    line_chart = pygal.Line()
    line_chart.title = 'Sales for the year 2019'
    line_chart.x_labels = map(str, x)
    line_chart.add('sales', sales)
    # line_chart = pygal.Line()
    # line_chart.title = 'Browser usage evolution (in %)'
    # line_chart.x_labels = map(str, range(2002, 2013))
    # line_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    # line_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    # line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    # line_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    #
    line_data = line_chart.render_data_uri()


    return render_template('index.html', pie_data = pie_data ,line_data=line_data)

@app.route('/about')
def about ():
    return render_template('about.html')

@app.route('/contact')
def contact ():
    return render_template('contact.html')
@app.route('/service')
def service():
    return render_template('service.html')




if __name__ == '__main__':
    app.run()
