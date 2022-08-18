from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo, Component
from ndn.transport.stream_socket import UnixFace

app= NDNApp()

print("...Advertising /node10")
@app.route('/node10')
def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest")
    content = "Replace this with a JSON"
    app.put_data(name, content=content.encode(), freshness_period=10000)

@app.route('/node10/cv')
def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest")
    content = "This is my CV from 10"
    app.put_data(name, content=content.encode(), freshness_period=10000)

if __name__ == '__main__':
    app.run_forever()
