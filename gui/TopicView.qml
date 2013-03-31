import Qt 4.7

Item {
    id: page 
    width: parent.width
    height: 200

    Text {
        id: title
        text: name; height: 40; width: parent.width/2
        font.pixelSize: 18; font.bold: true; color: "white"
        style: Text.Outline; styleColor: "black"
    }

    Rectangle {
        id: quitButton
        anchors.left: title.right
        height: 40; width: parent.width/2

        color: "grey"
        border.color: "white"
        MouseArea {
            anchors.fill: parent
            onClicked: {
                quit() //cannot call ListView.view.model.remove from here, why?
            }
        }
        Text { 
            anchors.centerIn: parent
            text: "Quit"
        }
    }

    function quit() {
        ListView.view.topicViewQuit(name)
        console.log("Topiv view quit: " + name)
        ListView.view.model.remove(index)  
    }

    ListView {
        id: eventList
        anchors.top: title.bottom
        rotation: -8
        width: page.width
        height: page.height/2
        model: events
        clip: true
        snapMode: ListView.SnapToItem
        delegate: EventListDelegate{message: msg}
        //delegate: Text{text: msg}
    }
    Component.onCompleted: {
        //ListView.view.scrollDown.connect(eventList.positionViewAtEnd)
        ListView.view.scrollDown.connect(scroll)
    }
    function scroll (){
        eventList.positionViewAtEnd()
    }

}








