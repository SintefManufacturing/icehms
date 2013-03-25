
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
            name: "firtst element"
        } 
        ListElement {
            name: "second element"
        } 
    }
   
Row {
    spacing: 30
    
    ListView {
        id: topiclist
        header: Text{text: "Available Topics"}
        width: page.width/2
        height: page.height
        model: topics
        delegate: TopicItem {}
    }  


    ListView {
        id: topicview
        width: page.width/2
        height: page.height

        model: displayedTopics
        delegate: TopicView {}
        function getView(name){
        }
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
}
function newevent(topicName, msg){
    var view = topicview.getView(topicName)
    if (name != null ) {
        view.addEvent(msg)
    }
}

}
