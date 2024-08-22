import React, { useState } from 'react';

// Monthly pricing tiers
const monthlyPricingTiers = [
  {
    id: 'starter',
    name: 'Starter',
    price: 9.99,
    badge: '✨ Free trial',
    features: [
      '7-day free trial',
      '1,000 tokens per month',
      '1 chatbot',
      '20 stored chats'
    ],
    buttonText: 'Buy plan',
    isPopular: false
  },
  {
    id: 'pro',
    name: 'Pro',
    price: 19.99,
    badge: '🚀 Most popular',
    features: [
      '5000 tokens per month',
      '5 chatbots',
      'Unlimited stored chats',
      'Integrations',
      'Document support'
    ],
    buttonText: 'Buy plan',
    isPopular: true
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: 29.99,
    features: [
      '20,000 tokens per month',
      'Unlimited chatbots',
      'Unlimited stored chats',
      'Train with websites or documents',
      'API access'
    ],
    buttonText: 'Buy plan',
    isPopular: false
  }
];

// Yearly pricing tiers (20% discount applied)
const yearlyPricingTiers = monthlyPricingTiers.map(tier => ({
  ...tier,
  price: Number((tier.price * 12 * 0.8).toFixed(2)), // 20% discount for yearly plans
}));

const PricingCard = () => {
  const [isYearly, setIsYearly] = useState(false);
  const pricingTiers = isYearly ? yearlyPricingTiers : monthlyPricingTiers;

  return (
    <div className="py-4 light:bg-slate-900" id='pricing'>
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="mt-2 text-4xl font-bold tracking-tight text-slate-900 light:text-slate-200 sm:text-5xl">
            Pricing Plans
          </h2>
          {/* Toggle */}
          <div className="mt-16 flex justify-center">
            <div className="rounded-full border border-slate-300 p-1 light:border-slate-300/20">
              <div className="flex text-xs font-semibold leading-5">
                <button 
                  className={`w-auto rounded-full px-3 py-1 focus:outline-none ${
                    !isYearly ? 'bg-blue-600 text-slate-200' : 'text-slate-800 light:text-slate-200'
                  }`}
                  onClick={() => setIsYearly(false)}
                >
                  Monthly
                </button>
                <button 
                  className={`rounded-full px-3 py-1 focus:outline-none ${
                    isYearly ? 'bg-blue-600 text-slate-200' : 'text-slate-800 light:text-slate-200'
                  }`}
                  onClick={() => setIsYearly(true)}
                >
                  Yearly
                </button>
              </div>
            </div>
          </div>
        </div>
        <div className="isolate mx-auto mt-10 grid max-w-md grid-cols-1 gap-y-8 lg:mx-0 lg:max-w-none lg:grid-cols-3 lg:gap-x-4">
          {pricingTiers.map((tier) => (
            <div
              key={tier.id}
              className={`flex flex-col justify-between rounded-3xl bg-slate-50 p-8 text-slate-900 ring-1 ${
                tier.isPopular ? 'ring-2 ring-blue-600' : 'ring-slate-300'
              } light:bg-slate-900 light:text-slate-200 light:ring-slate-300/20 ${
                tier.isPopular ? 'lg:z-10' : 'lg:mt-8'
              } xl:p-10`}
            >
              <div>
                <div className="flex items-center justify-between gap-x-4">
                  <h3 id={`tier-${tier.id}`} className="text-lg font-semibold leading-8">
                    {tier.name}
                  </h3>
                  {tier.badge && (
                    <p className="rounded-full bg-blue-600/10 px-2.5 py-1 text-xs font-semibold leading-5 text-blue-600">
                      {tier.badge}
                    </p>
                  )}
                </div>
                <p className="mt-6 flex items-baseline gap-x-1">
                  <span className="text-5xl font-bold tracking-tight">${tier.price}</span>
                  <span className="text-sm font-semibold leading-6 text-slate-700 light:text-slate-400">
                    /{isYearly ? 'year' : 'month'}
                  </span>
                </p>
                <ul className="mt-8 space-y-3 text-sm leading-6 text-slate-700 light:text-slate-400">
                  {tier.features.map((feature, index) => (
                    <li key={index} className="flex gap-x-3">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-6 w-5 flex-none text-blue-600"
                        viewBox="0 0 24 24"
                        strokeWidth="2"
                        stroke="currentColor"
                        fill="none"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                        <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0"></path>
                        <path d="M9 12l2 2l4 -4"></path>
                      </svg>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
              <a
                href="/"
                aria-describedby={`tier-${tier.id}`}
                className={`mt-8 block rounded-md px-3 py-2 text-center text-sm font-semibold leading-6 ${
                  tier.isPopular
                    ? 'bg-blue-600 text-blue-50 shadow-sm hover:bg-blue-700'
                    : 'text-blue-600 ring-1 ring-inset ring-blue-600 hover:bg-blue-600 hover:text-blue-50'
                }`}
              >
                {tier.buttonText}
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PricingCard;