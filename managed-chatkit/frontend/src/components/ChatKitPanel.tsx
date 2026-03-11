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
        uploadStrategy: {
          type: "hosted",
        },
        maxCount: 5,
        maxSize: 20 * 1024 * 1024,
        accept: {
          "application/pdf": [".pdf"],
          "image/*": [".png", ".jpg", ".jpeg", ".webp"],
        },
      },
    },
  });

  return (
    <div className="h-[100dvh] w-full bg-slate-100 dark:bg-slate-950">
      <div className="mx-auto h-full max-w-5xl">
        <ChatKit control={control} className="h-full" />
      </div>
    </div>
  );
}
