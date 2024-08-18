import React, { useState, useEffect } from 'react';
import { Sidebar } from '../../components';
import { ApiClient as apiClient } from '../../api/api';
import { useAuth } from '../../contexts/auth';
import { useNavigate } from "react-router-dom";

const Setting = () => {
  const [activeTab, setActiveTab] = useState('profile');
  const [botResponse, setBotResponse] = useState('');
  const [chatSessions, setChatSessions] = useState([
    { id: 1, title: "First Search" },
    { id: 2, title: "Product Inquiry" },
    { id: 3, title: "Size Comparison" },
  ]);
  const [activeSession, setActiveSession] = useState(1);
  const { user, loading } = useAuth();
  const navigate = useNavigate();
  
  // setSubscription({ "plan_type": "pro", "start_date": new Date(), "end_date": new Date(new Date().setDate(new Date().getDate() + 30))})
  const [subscription, setSubscription] = useState(null);
  const [showPlanSelection, setShowPlanSelection] = useState(false);
  

  useEffect(() => {
    // if (!loading && !user) {
    //   navigate("/login");
    // } else if (user) {
    //   fetchSubscription();
    // }
  }, [user, loading, navigate]);

  const fetchSubscription = async () => {
    try {
      const response = await apiClient.get('/subscriptions/current');
      setSubscription(response.data);
    } catch (error) {
      console.error('Error fetching subscription:', error);
    }
  };

  const handleSelectSession = (sessionId) => {
    setActiveSession(sessionId);
    setBotResponse(`You've selected chat session ${sessionId}`);
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    // Implement profile update logic here
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    // Implement password change logic here
  };

  const handleSubscribe = async (planType) => {
    // Implement subscription logic here
  };

  const handleCancelSubscription = async () => {
    // Implement subscription cancellation logic here
  };

  const handleDeleteAccount = async () => {
    // Implement account deletion logic here
  };


  const handleUpdatePlan = () => {
    setShowPlanSelection(true);
  };

  const handlePlanChange = async (planType) => {
    // Implement plan change logic here
    console.log(`Updating plan to ${planType}`);
    // After successful update, you might want to fetch the updated subscription
    // fetchSubscription();
    setShowPlanSelection(false);
  };

  const handleCancelPlan = async () => {
    // Implement plan cancellation logic here
    console.log('Cancelling plan');
    setSubscription(null);
  };


  //TODO Uncomment after authentication is ready
  // if (loading) {
  //   return <div>Loading...</div>;
  // }

  // if (!user) {
  //   return null;
  // }

  return (
    <div className='flex h-screen bg-gray-100'>
      <Sidebar
        chatSessions={chatSessions}
        onSelectSession={handleSelectSession}
        activeSession={activeSession}
      />
      <div className="flex flex-col flex-grow p-10 overflow-auto">
        <h1 className="text-3xl font-bold mb-6">Settings</h1>
        
        {/* Profile and Password Tabs */}
        <div className="rounded-lg overflow-hidden mb-8">
          <div className="flex border-b">
            <button
              className={`px-4 py-2 font-medium ${activeTab === 'profile' ? 'bg-gray-200 text-black' : 'text-gray-700'}`}
              onClick={() => setActiveTab('profile')}
            >
              Profile
            </button>
            <button
              className={`px-4 py-2 font-medium ${activeTab === 'password' ? 'bg-gray-200 text-black' : 'text-gray-700'}`}
              onClick={() => setActiveTab('password')}
            >
              Password
            </button>
          </div>
          <div className="p-6">
            {activeTab === 'profile' && (
              <form onSubmit={handleProfileUpdate}>
                <div className="mb-4">
                  <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
                    Username
                  </label>
                  <input
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    id="username"
                    type="text"
                    placeholder="Username"
                    value={user?.username}
                    disabled
                  />
                </div>
                <div className="mb-4">
                  <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
                    Email
                  </label>
                  <input
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    id="email"
                    type="email"
                    placeholder="Email"
                    value={user?.email}
                  />
                </div>
                <button
                  className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                  type="submit"
                >
                  Update Profile
                </button>
              </form>
            )}
            {activeTab === 'password' && (
              <form onSubmit={handlePasswordChange}>
                <div className="mb-4">
                  <label className="block text-gray-700 text-sm font-medium mb-2" htmlFor="currentPassword">
                    Current Password
                  </label>
                  <input
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    id="currentPassword"
                    type="password"
                    placeholder="Current Password"
                  />
                </div>
                <div className="mb-4">
                  <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="newPassword">
                    New Password
                  </label>
                  <input
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    id="newPassword"
                    type="password"
                    placeholder="New Password"
                  />
                </div>
                <div className="mb-6">
                  <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="confirmPassword">
                    Confirm New Password
                  </label>
                  <input
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    id="confirmPassword"
                    type="password"
                    placeholder="Confirm New Password"
                  />
                </div>
                <button
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                  type="submit"
                >
                  Change Password
                </button>
              </form>
            )}
          </div>
        </div>
        
        {/* Subscription Section */}
        <div className="rounded-lg p-6 mb-8 shadow">
          <h2 className="text-2xl font-bold mb-4">Subscription</h2>
          
          {subscription ? (
            <div>
              <p className="mb-2">Current Plan: {subscription.plan_type}</p>
              <p className="mb-2">Start Date: {new Date(subscription.start_date).toLocaleDateString()}</p>
              <p className="mb-4">End Date: {new Date(subscription.end_date).toLocaleDateString()}</p>
              <div className="flex space-x-4">
                <button
                  className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                  onClick={handleUpdatePlan}
                >
                  Update Plan
                </button>
                <button
                  className="bg-red-400 hover:bg-red-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                  onClick={handleCancelPlan}
                >
                  Cancel Plan
                </button>
              </div>
            </div>
          ) : (
            <div>
              <p className="mb-4">You don't have an active subscription.</p>
              <button
                className="bg-emerald-500 hover:bg-emerald-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                onClick={handleUpdatePlan}
              >
                Subscribe Now
              </button>
            </div>
          )}

          {showPlanSelection && (
            <div className="mt-4">
              <h3 className="text-lg font-semibold mb-2">Select a New Plan:</h3>
              <select
                className="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline"
                onChange={(e) => handlePlanChange(e.target.value)}
              >
                <option value="">Choose a plan</option>
                <option value="starter_monthly">Starter (Monthly)</option>
                <option value="pro_monthly">Pro (Monthly)</option>
                <option value="enterprise_monthly">Enterprise (Monthly)</option>
                <option value="starter_annual">Starter (Annual)</option>
                <option value="pro_annual">Pro (Annual)</option>
                <option value="enterprise_annual">Enterprise (Annual)</option>
              </select>
            </div>
          )}
        </div>
        
        {/* Danger Zone */}
        <div className="shadow-md rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4 text-red-600">Danger Zone</h2>
          <p className="mb-4">Deleting your account is permanent and cannot be undone.</p>
          <button
            className="bg-red-400 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            onClick={handleDeleteAccount}
          >
            Delete Account
          </button>
        </div>
      </div>
    </div>
  );
};

export default Setting;