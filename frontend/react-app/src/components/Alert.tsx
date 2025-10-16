import { ReactNode } from "react";
import Button from "./Button";

interface Props {
  children: ReactNode;
}

const Alert = ({ children }: Props) => {
  return (
    <>
      <div
        className={"alert alert-primary alert-dismissable fade show"}
        role="alert"
      >
        {children}
        <button
          type="button"
          className="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
        ></button>
      </div>
    </>
  );
};

export default Alert;
