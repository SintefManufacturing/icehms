import Qt 4.7

Item {
    id: msgitem
    property string message
height: 40
    Text {text: "TOTO" + message}
    ListView.onAdd: {
        //console.log("onAdd: A new item has been added")
    ListView.view.positionViewAtEnd()
    //ListView.positionViewAtEnd()
    }
}


