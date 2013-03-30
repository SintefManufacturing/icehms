import Qt 4.7

Item {
    id: page 
    width: parent.width
    height: 200

    Text {
        id: title
        text: name; x: 15; y: 8; height: 40; width: parent.width
        font.pixelSize: 18; font.bold: true; color: "white"
        style: Text.Outline; styleColor: "black"
    }

    ListView {
        id: eventList
        rotation: -8
        width: page.width
        height: page.height/2
        model: events
        //clip: true
        snapMode: ListView.SnapToItem
        delegate: EventListDelegate{message: msg}
        //delegate: Text{text: msg}
    }
    Component.onCompleted: {
        //ListView.view.scrollDown.connect(eventList.positionViewAtEnd)
        ListView.view.scrollDown.connect(scroll)
        console.log("connecting")
    }
    function scroll (){
        console.log("TESTING")
        eventList.positionViewAtEnd()
        console.log("TESTING2")
    }

}








