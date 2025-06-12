-- CreateTable
CREATE TABLE "InputWebhook" (
    "id" BIGSERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "type" TEXT NOT NULL,
    "key" TEXT NOT NULL,
    "description" TEXT,
    "org_id" BIGINT NOT NULL,

    CONSTRAINT "InputWebhook_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "InputWebhook_key_key" ON "InputWebhook"("key");

-- AddForeignKey
ALTER TABLE "InputWebhook" ADD CONSTRAINT "InputWebhook_org_id_fkey" FOREIGN KEY ("org_id") REFERENCES "Organization"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
