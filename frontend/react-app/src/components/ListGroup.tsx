import { useState } from "react";

interface Video {
  rowid: number;
  filename: string;
  uri: string;
  created: string;
}

interface Props {
  videos: Video[];
  heading: string;
  onSelectItem: (vid: Video) => void;
}

function ListGroup({ videos = [], heading, onSelectItem }: Props) {
  const [selectedIndex, setSelectedIndex] = useState(-1);

  return (
    <>
      <h3>{heading}</h3>
      {videos.length === 0 && <p>No videos found</p>}
      <ul className="list-group">
        {videos.map((video, index) => (
          <li
            className={
              selectedIndex === index
                ? "list-group-item active"
                : "list-group-item"
            }
            key={"video " + video.rowid}
            onClick={() => {
              setSelectedIndex(index);
              onSelectItem(video);
            }}
          >
            {video.uri}
          </li>
        ))}
      </ul>
    </>
  );
}

export default ListGroup;
