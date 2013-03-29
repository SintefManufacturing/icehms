
import Qt 4.7

Rectangle {
    id: page
    width: 800; height: 480
    color: "lightgray"
    signal topicDisplayed(string name)
    signal topicHidden(string name)

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
                console.log("onAdd method called !!!!!!!!!!!!!")
            }
            MouseArea {
                anchors.fill: parent
                onClicked: { page.focus = true; }
                onDoubleClicked: {
                    var idx = topiclistview.indexAt(mouseX, mouseY)
                    topiclistview.trigger(topics.get(idx).name); 
                    displayTopic(topics.get(idx).name)
                }
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
        console.log("New event from topic " + topicName )
        for (var i = 0; i < displayedTopics.count; i++){
            var item  = displayedTopics.get(i)
            if ( item.name == topicName )  {
                item.events.append({msg: newmsg})
                if ( item.count > 10 ) {
                    item.remove(0)
                }
                //item.events.positionViewAtEnd()
                //item.eventList.positionViewAtIndex(item.events.count-1, ListView.Contain)
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
        topicDisplayed(name)
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
        topicHidden(name)
        //console.log("Topic not found, could not remove displayed topic: " + name)
    }


}
