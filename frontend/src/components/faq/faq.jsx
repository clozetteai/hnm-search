import React, { useState } from 'react';

const FAQItem = ({ question, answer, isOpen, onToggle }) => (
  <div className="border-b border-gray-200 py-4">
    <button
      className="flex justify-between items-center w-full text-left"
      onClick={onToggle}
    >
      <span className="text-lg font-medium">{question}</span>
      <span className="text-2xl">{isOpen ? '-' : '+'}</span>
    </button>
    {isOpen && <p className="mt-2 text-gray-600">{answer}</p>}
  </div>
);

const FAQ = () => {
  const [openIndex, setOpenIndex] = useState(null);

  const faqData = [
    {
      question: "What is Clozette.AI?",
      answer: "Clozette.AI is an advanced AI-powered platform that helps fashion retailers and brands optimize their inventory management and product recommendations using SQL and machine learning technologies."
    },
    {
      question: "Is Clozette.AI free to use?",
      answer: "Clozette.AI offers a free trial period for new users. After the trial, we have various pricing plans to suit different business needs. Check our pricing page for more details."
    },
    {
      question: "How does Clozette.AI use SQL?",
      answer: "Clozette.AI leverages SQL to efficiently query and analyze large datasets of fashion inventory and sales data, enabling powerful insights and predictions for your business."
    },
    {
      question: "Do I need technical knowledge to use Clozette.AI?",
      answer: "No, Clozette.AI is designed to be user-friendly for fashion professionals without requiring deep technical knowledge. Our interface translates complex data into actionable insights."
    },
    {
      question: "Can Clozette.AI integrate with my existing systems?",
      answer: "Yes, Clozette.AI is built to integrate seamlessly with most popular e-commerce platforms and inventory management systems. Our team can assist with custom integrations if needed."
    },
    {
      question: "How secure is my data with Clozette.AI?",
      answer: "We take data security very seriously. Clozette.AI uses industry-standard encryption and security protocols to ensure your data is protected at all times. We are compliant with major data protection regulations."
    },
    {
      question: "What kind of support does Clozette.AI offer?",
      answer: "Clozette.AI provides comprehensive support including documentation, video tutorials, email support, and dedicated account managers for enterprise clients. We're committed to ensuring your success with our platform."
    }
  ];

  return (
    <div className="max-w-3xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <h2 className="text-base text-gray-600 font-semibold tracking-wide uppercase">FAQ</h2>
        <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
          Frequently Asked Questions
        </p>
        <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">
          Find answers to commonly asked questions about Clozette.AI
        </p>
      </div>
      <div className="mt-8">
        {faqData.map((item, index) => (
          <FAQItem
            key={index}
            question={item.question}
            answer={item.answer}
            isOpen={index === openIndex}
            onToggle={() => setOpenIndex(index === openIndex ? null : index)}
          />
        ))}
      </div>
    </div>
  );
};

export default FAQ;