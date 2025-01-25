require("dotenv").config();
const { GenerativeModel } = require("google-generativeai");

// Function to convert text to markdown-style blockquote
function toMarkdown(text) {
  text = text.replace(/•/g, "  *"); // Replace bullet points with asterisks
  return `> ${text.split("\n").join("\n> ")}`; // Indent all lines with `>`
}

// Load the API key from the .env file
const googleApiKey = process.env.GEMINI_API_KEY;

// Configure the generative model
const genai = new GenerativeModel();
genai.configure({ apiKey: googleApiKey });

// Define the system prompt
const systemPrompt = {
  text: "You are a medical AI assistant. You should predict the reaction between the medicine and its effect on the body.",
};

// Tool to maintain a list of medicines
let medicineList = [];
function medicineTool(medicine) {
  const med = medicine.toLowerCase().trim();
  if (!medicineList.includes(med)) {
    medicineList.push(med);
  }
  return medicineList;
}

// Define the medicine function configuration
const medicineFunction = {
  name: "medicine_tool",
  description:
    "Gets the list of medicines. Call this whenever you want to get the list of medicines, for example, when the user asks for a list of medicines.",
  parameters: {
    type: "object",
    properties: {
      medicine: {
        type: "string",
        description: "The medicine name",
      },
    },
    required: ["medicine"],
    additionalProperties: false,
  },
};

// Define tool configuration
const toolConfig = {
  functionCallingConfig: {
    mode: "ANY",
    allowedFunctionNames: ["medicine_function"],
  },
};

// Message function to interact with the AI
async function messageGemini(...userPrompt) {
  const messages = [
    { role: "system", content: systemPrompt.text },
    { role: "user", content: userPrompt.join(", ") },
  ];

  try {
    const response = await genai.generateContent({
      messages: messages,
      modelName: "gemini-1.5-flash",
      systemInstruction: systemPrompt.text,
      toolConfig: toolConfig,
    });
    return response.text;
  } catch (error) {
    console.error("Error generating content:", error);
  }
}

// Example usage
(async () => {
  medicineTool("paracetamol");
  medicineTool("ibuprofen");
  medicineTool("aspirin");

  const responseText = await messageGemini(
    "paracetamol",
    "ibuprofen",
    "aspirin"
  );
  console.log(toMarkdown(responseText));
})();
