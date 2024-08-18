import React from "react";

const promptCards = [
  {
    title: "Screenwriter",
    description: "I want you to act as a screenwriter. You will develop an engaging and creative script for either a feature length film or a Web Series that can captivate its viewers.",
    prompt: "Act as a screenwriter and create a script for a short film about artificial intelligence."
  },
  {
    title: "Debater",
    description: "I want you to act as a debater. I will provide you with some topics related to current events and your task is to research both sides of the debates.",
    prompt: "Act as a debater and present arguments for and against the use of renewable energy sources."
  },
  {
    title: "Cyber Security Specialist",
    description: "I want you to act as a cyber security specialist. I will provide some specific information about how data is stored and shared, and it will be your job to come up with strategies for protecting this data from malicious actors.",
    prompt: "Act as a cyber security specialist and suggest strategies to protect a company's customer data from potential breaches."
  },
  {
    title: "Influencer",
    description: "I want you to act as a social media influencer. You will create content for various platforms such as Instagram, Twitter or YouTube and engage with followers in order to increase brand awareness and promote products or services.",
    prompt: "Act as a social media influencer and create a campaign to promote sustainable fashion."
  }
];

const PromptCard = ({ handlePromptCardClick }) => {
  return (
    <div className="max-w-5xl mx-auto px-4">
      <ul className="grid grid-cols-1 sm:grid-cols-2 gap-6 text-slate-900 light:text-slate-200">
        {promptCards.map((card, index) => (
          <li key={index} className="group rounded-lg bg-slate-50 shadow transition-colors duration-300 hover:bg-blue-600 light:bg-slate-900 light:hover:bg-blue-600">
            <div
              className="flex cursor-pointer items-center space-x-4 truncate p-4"
              onClick={() => handlePromptCardClick(card.prompt)}
            >
              <div className="flex-shrink-0">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6"
                  strokeWidth="2"
                  stroke="currentColor"
                  fill="none"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                  <path d="M14 6l7 7l-4 4"></path>
                  <path d="M5.828 18.172a2.828 2.828 0 0 0 4 0l10.586 -10.586a2 2 0 0 0 0 -2.829l-1.171 -1.171a2 2 0 0 0 -2.829 0l-10.586 10.586a2.828 2.828 0 0 0 0 4z"></path>
                  <path d="M4 20l1.768 -1.768"></path>
                </svg>
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-medium text-slate-900 truncate transition-colors duration-300 group-hover:text-slate-50 light:text-slate-200">
                  {card.title}
                </h3>
                <p className="mt-1 text-sm text-slate-500 truncate transition-colors duration-300 group-hover:text-slate-300">
                  {card.description}
                </p>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PromptCard;