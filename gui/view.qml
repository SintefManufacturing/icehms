
import Qt 4.7

Rectangle {
    id: page
    width: 800; height: 480
    color: "lightgray"

    ListModel {
        id: topics
    }

    ListModel {
        id: displayedTopics
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
            var idx = topiclistview.indexAt(mouseX, mouseY)
            topiclistview.trigger(topics.get(idx).name); 
            displayTopic(topics.get(idx).name)
        }
        //onClicked: { page.focus = true; myText.openSoftwareInputPanel(); }
/*
    }
    onItemtrigger: {
        console.log("Item trigger at list level")
*/
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
    console.log("New event from topic " + topicName + ": " + newmsg)
    for (var i = 0; i < displayedTopics.count; i++){
        var item  = displayedTopics.get(i)
        console.log( "item: " + item.name + " topic: " + topicName )  
        if ( item.name == topicName )  {
            item.events.append({msg: newmsg})
            return;
        }
    }
    console.log("Topic not found, could add event to topic: " + topicName)
}

function displayTopic(name){
    console.log("displaying topic: " + name)
    for (var i = 0; i < displayedTopics.count; i++){
        if ( displayedTopics.get(i).name == name ) {
            return;
        }
    }
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
