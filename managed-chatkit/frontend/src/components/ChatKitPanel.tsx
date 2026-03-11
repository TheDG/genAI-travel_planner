import { useMemo } from "react";
import { ChatKit, useChatKit } from "@openai/chatkit-react";
import { createClientSecretFetcher, workflowId } from "../lib/chatkitSession";

export function ChatKitPanel() {
  const getClientSecret = useMemo(
    () => createClientSecretFetcher(workflowId),
    []
  );

  const { control } = useChatKit({
    api: {
      getClientSecret,
    },
    composer: {
      attachments: {
        enabled: true,
        maxCount: 5,
        maxSize: 20 * 1024 * 1024,
        accept: {
          "image/*": [".png", ".jpg", ".jpeg", ".gif", ".webp"],
          "application/pdf": [".pdf"],
          "text/plain": [".txt"],
          "text/markdown": [".md"],
          "text/csv": [".csv"],
          "application/json": [".json"],
        },
      },
    },
  });

  return <ChatKit control={control} className="h-full w-full" />;
}
