import Qt 4.7

Item {
    id: page 
    property int itwidth 
    signal itemtrigger (string name)
    width: parent.width
    height: 40 

    Component.onCompleted: {
        //console.log("TopicItem completed: " + name)
        //ListView.view.trigger.connect(page.trigger)
/*
    }
    onTrigger: {
        console.log("TopicItem clicked: " + name)
        //parent.trigger.connect(page.trigger)
*/
    }
    MouseArea {
        anchors.fill: parent
        onClicked: { page.focus = true; }
        onDoubleClicked: { itemtrigger(name); }
        //onClicked: { page.focus = true; myText.openSoftwareInputPanel(); }
    }

    Text {
        text: name; x: 15; y: 8; height: 40; width: 370
        font.pixelSize: 18; font.bold: true; color: "white"
        style: Text.Outline; styleColor: "black"
        rotation: -8
    }

}




