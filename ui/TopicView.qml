import QtQuick 1.0

Item {
    id: page 
    width: parent.width
    height: 300
    anchors.left: parent.left
    anchors.leftMargin: 12

    Text {
        id: title
        text: name; height: 40; width: parent.width/2
        font.pixelSize: 18; font.bold: true; color: "white"
        style: Text.Outline; styleColor: "black"
    }

    Rectangle {
        id: quitButton
        anchors.right: parent.right
        //anchors.rightMargin: 5 
        height: 40; width: 100 

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
        width: page.width 
        height: page.height/2
        model: events
        //clip: true
        snapMode: ListView.SnapToItem
        delegate: EventListDelegate{message: msg}
        MouseArea {
            id:mymousearea
            anchors.fill: parent
            hoverEnabled: true
        }
        states: State { // Only show the scrollbars when mouse over FIXME broken!!
            name: "ShowBars"
            when: mymousearea.containsMouse
            //when: topiclistview.movingVertically || topiclistview.movingHorizontally
            PropertyChanges { target: verticalScrollBar; opacity: 0.3 }
        }
        transitions: Transition {
            NumberAnimation { properties: "opacity"; duration: 400 }
        }
    }

   ScrollBar {
        id: verticalScrollBar
        width: 12; height: eventList.height-12
        anchors.top: eventList.top
        anchors.left: eventList.left
        opacity: 0
        orientation: Qt.Vertical
        position: eventList.visibleArea.yPosition
        pageSize: eventList.visibleArea.heightRatio
    }
/*
   ScrollBar {
        id: horizontalScrollBar
        width: eventList.width-12; height: 12
        anchors.bottom: eventList.bottom
        opacity: 1
        orientation: Qt.Horizontal
        position: eventList.visibleArea.xPosition
        pageSize: eventList.visibleArea.widthRatio
    }
*/


    Component.onCompleted: {
        //ListView.view.scrollDown.connect(eventList.positionViewAtEnd)
        ListView.view.scrollDown.connect(scroll)
    }

    function scroll (){
        eventList.positionViewAtEnd()
    }

}








