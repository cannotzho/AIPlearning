import D from "../assets/dog.avif";
import { getImageURL } from "../utils/img-utils";

interface Props {
  image_url?: string;
  date_created?: string;
  frame_timestamp?: string;
}

function Card({
  image_url = "dog.avif",
  date_created,
  frame_timestamp,
}: Props) {
  return (
    <div className="card">
      <img src={getImageURL(image_url)} className="card-img-top" alt="..." />
      <div className="card-body">
        <h5 className="card-title">{frame_timestamp}</h5>
        <p className="card-text">{date_created}</p>
      </div>
    </div>
  );
}

export default Card;
