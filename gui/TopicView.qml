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


        TextEdit {
            id: myText
            x: 0; y: 36; width: parent.width; height: parent.height - title.height
            smooth: true
            font.pixelSize: 24
            readOnly: false
            rotation: -8
            text: "TOTOTO" 
        }
    }








