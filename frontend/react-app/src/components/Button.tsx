interface Props {
  color?: "primary" | "secondary" | "danger";
  children: string;
  onClick: () => void;
}

function Button({ color = "primary", children, onClick }: Props) {
  return (
    <>
      <button className={"btn btn-" + color + " my-2"} onClick={onClick}>
        {children}
      </button>
    </>
  );
}

export default Button;
