const { Client, LogLevel } = require("@notionhq/client")
require('dotenv').config()

const notion = new Client({ auth: process.env.NOTION_TOKEN })

const databaseId = process.env.NOTION_DATABASE_ID

async function addItem(text) {
  try {
    const response = await notion.pages.create({
      parent: { database_id: databaseId },
      properties: {
        title: {
          title:[
            {
              "text": {
                "content": text
              }
            }
          ]
        }
      },
    })
    console.log(response)
    console.log("Success! Entry added.")
  } catch (error) {
    console.error(error.body)
  }
}

// todo: hacer andar 
async function getPage(pageId) {
  try {
    const response = await notion.pages.retrieve({ database_id: "c77d89e33f5540aea9ecdd377992b692", page_id: "c115a71c41614502af1a18d56ee62afc"});
    console.log(response)
    console.log("ahi ta la página")
  } catch (error) {
    console.error(error.body)
  }
}

async function getChildrenBlock(blockId) {
  try{
    const blockId = '8d629ab8014a449e91c79d7ab6b33e75';
    const response = await notion.blocks.children.list({
      block_id: blockId,
    });
    console.log(response);
  }catch (error){
    console.log(error.body)
  }
  
}


async function getDataBase(pageId) {
  try {
    const response = await notion.pages.retrieve({ page_id: pageId });
    console.log(response)
    console.log("ahi ta la página")
  } catch (error) {
    console.error(error.body)
  }
}
// addItem("Yurts in Big Sur, California")
// getPage(process.env.NOTION_PAGE_ID)
getChildrenBlock("")