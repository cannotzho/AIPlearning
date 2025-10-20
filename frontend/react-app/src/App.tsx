import { ChangeEvent, useEffect, useState } from "react";
import Grid, { Video } from "./components/Grid";
import ListGroup from "./components/ListGroup";
import Searchbar from "./components/Searchbar";
import UploadBtn from "./components/UploadBtn";

function App() {
  const [displayedVideos, setDisplayedVideos] = useState<Video[]>([]);
  const [selectedVideo, setSelectedVideo] = useState<Video>();

  const getVideos = () => {
    fetch("/api/videos/")
      .then((response) => response.json())
      .then((data) => setDisplayedVideos(data));
  };

  useEffect(() => {
    getVideos();
  }, []);

  const handleSearch = (videos: Video[]) => {
    setDisplayedVideos(videos);
    if (videos) {
      setSelectedVideo(videos[0]);
    } else {
      console.log("set video failed");
    }
  };

  return (
    <div className="container-xxl" style={{ maxHeight: "100vh" }}>
      <div className="row">
        <div
          className="col-4 bg-secondary rounded-4 mt-2 vh-100 overflow-auto"
          style={{ maxHeight: "100vh" }}
          key="sidebar"
        >
          {/* Column for sidebar */}
          {/* Upload Button */}
          <UploadBtn upload_route="/api/process" />
          {/* Searchbar */}
          <Searchbar
            option1="Detected Objects"
            option2="Filename"
            handleResponse={handleSearch}
          />
          {/* Video List*/}
          <ListGroup
            videos={displayedVideos}
            heading="Processed Videos"
            onSelectItem={setSelectedVideo}
          />
        </div>
        <div
          className="col-8 mt-2 bg-info rounded-4 vh-100"
          style={{ maxHeight: "100vh" }}
          key="main"
        >
          {" "}
          {/* Column for main content */}
          <Grid video={selectedVideo}>Video Details</Grid>
        </div>
      </div>
    </div>
  );
}

export default App;
