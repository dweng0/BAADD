import React, { useState, useRef } from "react";
import { Box, Text, useInput } from "ink";

type TextInputProps = {
  placeholder?: string;
  onSubmit: (value: string) => void;
  onBack?: () => void;
  isActive?: boolean;
};

export default function TextInput({
  placeholder = "",
  onSubmit,
  onBack,
  isActive = true,
}: TextInputProps) {
  const [value, setValue] = useState("");
  const valueRef = useRef("");

  useInput(
    (input, key) => {
      if (key.return) {
        onSubmit(valueRef.current);
        return;
      }

      if (key.escape && onBack) {
        onBack();
        return;
      }

      if (key.backspace || key.delete) {
        valueRef.current = valueRef.current.slice(0, -1);
        setValue(valueRef.current);
        return;
      }

      if (!key.ctrl && !key.meta && input) {
        valueRef.current = valueRef.current + input;
        setValue(valueRef.current);
      }
    },
    { isActive },
  );

  return (
    <Box>
      <Text color="cyan">{value || placeholder}</Text>
      {isActive && <Text color="gray">_</Text>}
    </Box>
  );
}
