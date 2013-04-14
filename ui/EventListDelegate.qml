import QtQuick 1.0

Item {
    id: msgitem
    property string message
    height: 30
    Text {text: message}
    ListView.onAdd: {
        //console.log("onAdd: A new item has been added")
        //ListView.view.positionViewAtEnd()
        //ListView.view.positionViewAtIndex(ListView.count -1,ListView.Contain ) //crash application
        //ListView.view.currentIndex = item.events.count-1
        //ListView.view.currentIndex = index 
        //console.log("scrolled to end")
    }
    Component.onCompleted: {
        //ListView.view.currentIndex = index 
        //ListView.view.positionViewAtEnd()
        //console.log("scrolled to end 2")
    }
    //Component.onCompleted: ListView.view.positionViewAtEnd() // crashes application
}


