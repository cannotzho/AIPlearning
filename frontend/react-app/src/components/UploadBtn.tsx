import React from "react";

interface Props {
  upload_route: string;
}

const UploadBtn = ({ upload_route }: Props) => {
  return (
    <>
      <form action={upload_route} method="POST" encType="multipart/form-data">
        <div className="input-group mb-3">
          <input
            type="file"
            className="form-control"
            id="videoInput"
            name="video"
          />
          <label className="input-group-text" htmlFor="videoInput">
            <button type="submit" className="btn btn-primary">
              Upload
            </button>
          </label>
        </div>
      </form>
    </>
  );
};

export default UploadBtn;
