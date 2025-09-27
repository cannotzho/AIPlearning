Notes

This file is just for me to have a space to log my thoughts about the project as I'm having them, so that I don't forget anything.

Will organize things as I go along.

BACKEND

-Create RESTful API using python web framework - need to understand what this means
according to gemini... REST has the following characteristics:

-Client-Server Architecture: The client and server are separate, allowing for independent development and scaling.

-Statelessness: Each client request to the server contains all necessary information, and the server does not store any client context between requests. > i.e. the server should be able to to respond to each request independently regardless of requests which came before?

-Cacheability: Responses can be explicitly or implicitly marked as cacheable to improve performance and network efficiency.

-Uniform Interface: This is a core principle, ensuring a standardized way for clients to interact with resources. It involves:

    -Resource Identification: Resources are identified by unique URLs.

    -Resource Manipulation through Representations: Clients interact with resources by exchanging representations (e.g., JSON, XML) of those resources. > reducing size of information that's being passed around?

    -Self-descriptive Messages: Each message contains enough information to be processed, including HTTP methods (GET, POST, PUT, DELETE) and status codes.

    -Hypermedia as the Engine of Application State (HATEOAS): Messages include links to related resources, guiding the client through the API.

-Layered System: The architecture allows for hierarchical layers (e.g., load balancers, proxies) that are transparent to the client. > will understand what this means later

-Code-on-Demand (Optional): Servers can temporarily extend or customize client functionality by transferring executable code. > interesting

What are API endpoints?
-URLs for an API client to get resources

Looks like I will have to go through a flask tutorial first to understand Python web frameworks before understanding how endpoints are defined

I'll create a folder called Examples to keep all the files I create for my own learning that's not directly related to the tasks

Finished the Flask app basic tutorial - that was pretty useful. It covered a bit of db stuff as well which is gonna be useful later

I can probably set up the skeleton of the backend for task 1a now. First thing i want to do is create the venv for this app

Seems like the main things the app is supposed to do is detect objects from submitted videos and then have a database of entries summarizing their detected objects. db entries should have the following: video file name, detected objects, frame timestamps, and created timestamp

hmm since the assignment split the tasks into backend frontend i guess i will focus on the functionality first and check by manually uploading some test videos first

    b) Implement video processing capabilities:
    * Use lightweight, CPU-friendly models for key frame selection (e.g., scene change detection using OpenCV)
    * Implement basic object detection using a lightweight model (e.g., MobileNet SSD via OpenCV's DNN module)
    * Generate text embeddings for detected objects using a lightweight embedding model (e.g., sentence-transformers/all-MiniLM-L6-v2)
    * Create a summary of detected objects and their timestamps

find out more about lightweight models - presumably key frame selection is a method to filter out any video frames which would be uninteresting?
to rephrase the broken down tasks within video processing, its:
1 - identify key frames to perform analysis
2 - object detection on an image (aka the chosen frame)
3 - generate text embeddings for objects
4 - summarize detected objects and their timestamps

no. 2 is maybe the most interesting one right now and kind of the basis of the whole video processing so i'll figure that out first

Following the example given in the task, i've looked into the mobile net model and it seems like setting up simple object deetection with a webcam feed is quite straightforward - i will attempt this first for my own learning and then see how i can apply this within the app later. As far as lightweight models go, there are quite a number to choose from but I will just choose this first. Architecturally if i want to change the model later on it should be possible by simply switching out the scripts that the endpoints are referring to. However from a preliminary look, R-CNN is definitely out of the question due to the computing requirements so it is at least narrowed down to SSD or YOLO approaches which both look at the image only once, greatly reducing the computing load