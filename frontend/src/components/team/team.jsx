import React from 'react';

const TeamMember = ({ name, title, imageSrc, x, github }) => (
  <div className="flex flex-col items-center">
    <div className="relative w-48 h-48 mb-4">
      <img
        src={imageSrc}
        alt={name}
        className="rounded-full w-full h-full object-cover"
      />
      <div className="absolute bottom-0 right-0 w-full h-full rounded-full border-2 border-black -mb-2 -mr-2"></div>
    </div>
    <h3 className="text-xl font-bold">{name}</h3>
    <p className="text-gray-600">{title}</p>
    <div className="mt-2 flex space-x-2">
      <a href={x} className="text-gray-400 hover:text-gray-600">
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
        </svg>
      </a>
      <a href={github} className="text-gray-400 hover:text-gray-600">
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
        </svg>
      </a>
    </div>
  </div>
);

const OurTeam = () => {
  const teamMembers = [
    { name: "Siddhant Prateek", title: "Software Engineer (Infra)", imageSrc: "https://avatars.githubusercontent.com/u/43869046?v=4", x: "https://x.com/siddhantprateek", github: "https://github.com/siddhantprateek" },
    { name: "Anindyadeep Sanigrahi", title: "Data Scientist", imageSrc: "https://avatars.githubusercontent.com/u/58508471?v=4", x: "https://x.com/AnindyadeepS", github: "https://github.com/Anindyadeep" },
    { name: "Pratyush Patnaik", title: "ML Engineer", imageSrc: "https://avatars.githubusercontent.com/u/78687109?v=4", x: "", github: "https://github.com/Pratyush-exe" },
  ];

  return (
    <div className="max-w-6xl mx-auto my-20 px-4">
      <div className="flex justify-between items-center mb-12">
        <h2 className="text-4xl font-bold">OUR TEAM</h2>
        <div className="flex space-x-4">
          <button className="text-3xl">←</button>
          <button className="text-3xl">→</button>
        </div>
      </div>
      <div className="flex justify-between">
        {teamMembers.map((member, index) => (
          <TeamMember key={index} {...member} />
        ))}
      </div>
    </div>
  );
};

export default OurTeam;