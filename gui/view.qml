
import Qt 4.7

Rectangle {
    id: page
    width: 800; height: 480
    color: "lightgray"

    ListModel {
        id: topics
        ListElement {
            name: "topic"
        } 
        ListElement {
            name: "topic 2"
        } 
        ListElement {
            name: "topic 3"
        } 
    }

     ListModel {
        id: displayedTopics
        ListElement {
            name: "Conveyor::State"
            events: [
                ListElement { msg: "first event" },
                ListElement { msg: "second event" }
            ]
        } 
        ListElement {
            name: "MakinoCell::PullRequest"
            events: [
                ListElement { msg: "first event" },
                ListElement { msg: "second event" }
            ]
        } 
        function getView(name){
        }
    }
   
Row {
    spacing: 30
    
    ListView {
        id: topiclistview
        signal trigger (string name)
        header: Text{text: "Available Topics"}
        width: page.width/2
        height: page.height
        model: topics
        delegate: TopicItem {}
        Component.onCompleted: {
            //console.log("Connecting signals")
            //topiclistview.trigger.connect(delegate.trigger)
            //console.log("signals connected")
        }
        ListView.onAdd: {
            console.log("item added")
        }
    MouseArea {
        anchors.fill: parent
        onClicked: { page.focus = true; }
        onDoubleClicked: {
            console.log("double click i listview")
            var idx = topiclistview.indexAt(mouseX, mouseY)
            console.log("index: " + idx)
            topiclistview.trigger(topics.get(idx).name); 
            displayTopic(topics.get(idx).name)
        }
        //onClicked: { page.focus = true; myText.openSoftwareInputPanel(); }
    }
    }  


    ListView {
        id: topicview
        width: page.width/2
        height: page.height
        //clip: true

        model: displayedTopics
        delegate: TopicView {}
    }

}

function addTopic(name){
    console.log("Adding topic: " + name)
    topics.append({"name": name})
}

function removeTopic(name){
    console.log("Removing topic: " + name)
    for (var i = 0; i < topics.count; i++){
        if ( topics.get(i).name == name ) {
            topics.remove(i)
            return;
        }
    }
    console.log("Topic not found, could not remove topic: " + name)
}

function newEvent(topicName, newmsg){
    for (var i = 0; i < displayedTopics.count; i++){
        var item  = displayedTopics.get(i)
        if ( item.name == topicName )  {
            item.events.append({msg: newmsg})
            return;
        }
    }
    console.log("Topic not found, could add event to topic: " + topicName)
}

function displayTopic(name){
    console.log("displaying topic: " + name)
    displayedTopics.append({"name": name, events: [{msg: "empty"}]})
}
function hideTopic(name){
    console.log("hiding topic: " + name)
    for (var i = 0; i < displayedTopics.count; i++){
        if ( displayedTopics.get(i).name == name ) {
            displayedTopics.remove(i)
            return;
        }
    }
    console.log("Topic not found, could not remove displayed topic: " + name)
}


}
