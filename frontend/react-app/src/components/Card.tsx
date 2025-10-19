interface Props {
  image_url?: string;
  frame_number: number;
  date_created?: string;
  frame_timestamp?: string;
}

function Card({
  image_url = "placeholder",
  frame_number = 0,
  date_created,
  frame_timestamp,
}: Props) {
  return (
    <div className="card m-4" style={{ width: 350, height: 300 }}>
      <img
        src={"/api/keyframes/" + image_url + "/" + frame_number}
        className="card-img-top img-fluid"
        alt="..."
        style={{ height: 200 }}
      />
      <div className="card-body">
        <h5 className="card-title">{frame_timestamp}</h5>
        <p className="card-text">{date_created}</p>
      </div>
    </div>
  );
}

export default Card;
