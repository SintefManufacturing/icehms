
import QtQuick 1.0

Rectangle {
    id: page
    width: 800; height: 480
    color: "lightgray"
    signal topicDisplayed(string name)
    signal topicHidden(string name)
    signal scrollToBottom

    ListModel {
        id: topics
    }

    ListModel {
        id: displayedTopics
    }
   
    ListView {
        id: topiclistview
        signal trigger (string name)
        header: Text{text: "Available Topics"}
        width: 200 
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
    ScrollBar {
        id: topiclistviewScrollBar
        width: 12; height: topiclistview.height
        anchors.top: topiclistview.top
        anchors.left: topiclistview.left
        opacity: 1
        orientation: Qt.Vertical
        position: topiclistview.visibleArea.yPosition
        pageSize: topiclistview.visibleArea.heightRatio
    }
    ListView {
        id: topicview
        anchors.left: topiclistview.right
        height: page.height
        width: page.width - topiclistview.width
        //clip: true
        model: displayedTopics
        delegate: TopicView {}
        signal scrollDown
        signal topicViewQuit(string name)
    }
    ScrollBar {
        id: topicviewScrollBar
        width: 12; height: topicview.height
        anchors.top: topicview.top
        anchors.left: topicview.left
        opacity: 1
        orientation: Qt.Vertical
        position: topicview.visibleArea.yPosition
        pageSize: topicview.visibleArea.heightRatio
    }


    Component.onCompleted: {
        topicview.topicViewQuit.connect(topicHidden)
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
        //console.log("New event from topic " + topicName )
        for (var i = 0; i < topicview.count; i++){
            
        }
        for (var i = 0; i < displayedTopics.count; i++){
            var item  = displayedTopics.get(i)
            if ( item.name == topicName )  {
                item.events.append({msg: newmsg})
                if ( item.events.count > 10 ) {
                    item.events.remove(0)
                }
                topicview.scrollDown() //activate event in listview
                return;
            }
        }
        console.log("Topic not found, could not add event to topic: " + topicName)
    }

    function displayTopic(name){
        console.log("displaying topic: " + name)
        for (var i = 0; i < displayedTopics.count; i++){
            if ( displayedTopics.get(i).name == name ) {
                return;
            }
        }
        topicDisplayed(name)
        //displayedTopics.append({"name": name, events: [{msg: "empty"}]})
        displayedTopics.append({"name": name, events: [{msg: "No events yet"}]})
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
