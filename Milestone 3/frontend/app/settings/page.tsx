"use client";

import { useState } from "react";
import { Bell, Lock, User, FileText, Eye, EyeOff } from "lucide-react";

export default function Settings() {
  const [activeTab, setActiveTab] = useState<"profile" | "security" | "notifications" | "preferences">("profile");
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    fullName: "John Doe",
    email: "john@example.com",
    institution: "State University",
    role: "Professor",
    bio: "Teaching computer science and AI",
  });

  const [passwordData, setPasswordData] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
  });

  const [notifications, setNotifications] = useState({
    emailNotifications: true,
    studentQuestions: true,
    assessmentGrading: false,
    weeklyDigest: true,
    systemUpdates: true,
  });

  const [preferences, setPreferences] = useState({
    theme: "light",
    language: "English",
    defaultView: "dashboard",
    autoSave: true,
  });

  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setPasswordData((prev) => ({ ...prev, [name]: value }));
  };

  const handleNotificationChange = (key: keyof typeof notifications) => {
    setNotifications((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="border-b border-[#e7edf3] px-10 py-6">
        <h1 className="text-[32px] font-bold text-[#0d141b] leading-tight">
          Settings
        </h1>
        <p className="text-[#4c739a] text-sm mt-1">
          Manage your account settings and preferences
        </p>
      </div>

      <div className="flex flex-1">
        {/* Settings Sidebar */}
        <div className="w-64 border-r border-[#e7edf3] bg-slate-50 p-6">
          <div className="space-y-2">
            <button
              onClick={() => setActiveTab("profile")}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left font-medium transition-colors ${activeTab === "profile"
                ? "bg-[#e7edf3] text-[#0d141b]"
                : "text-[#4c739a] hover:bg-slate-100"
                }`}
            >
              <User className="w-5 h-5" />
              Profile
            </button>
            <button
              onClick={() => setActiveTab("security")}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left font-medium transition-colors ${activeTab === "security"
                ? "bg-[#e7edf3] text-[#0d141b]"
                : "text-[#4c739a] hover:bg-slate-100"
                }`}
            >
              <Lock className="w-5 h-5" />
              Security
            </button>
            <button
              onClick={() => setActiveTab("notifications")}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left font-medium transition-colors ${activeTab === "notifications"
                ? "bg-[#e7edf3] text-[#0d141b]"
                : "text-[#4c739a] hover:bg-slate-100"
                }`}
            >
              <Bell className="w-5 h-5" />
              Notifications
            </button>
            <button
              onClick={() => setActiveTab("preferences")}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left font-medium transition-colors ${activeTab === "preferences"
                ? "bg-[#e7edf3] text-[#0d141b]"
                : "text-[#4c739a] hover:bg-slate-100"
                }`}
            >
              <FileText className="w-5 h-5" />
              Preferences
            </button>
          </div>
        </div>

        {/* Settings Content */}
        <div className="flex-1 p-10">
          <div className="max-w-2xl">
            {/* Profile Tab */}
            {activeTab === "profile" && (
              <div className="space-y-8">
                <div>
                  <h2 className="text-[22px] font-bold text-[#0d141b] mb-6">
                    Profile Information
                  </h2>

                  {/* Profile Picture */}
                  <div className="mb-8 pb-8 border-b border-[#e7edf3]">
                    <p className="text-[#0d141b] font-medium mb-4">Profile Picture</p>
                    <div className="flex items-center gap-6">
                      <div
                        className="w-24 h-24 rounded-full bg-center bg-cover border-4 border-[#e7edf3]"
                        style={{
                          backgroundImage:
                            'url("https://lh3.googleusercontent.com/aida-public/AB6AXuCzJxrTUrwy0B6qlDVEKIbo9SgK6LaU_t7vLosY8oqZfWrs8yN00-as4XmXOp_kJX1aIMKI6oh4yHS7gbfWi-pQPus_16z5ioDCwkqw5kHxiqV62xdUsQvkZCn3XA_iWrd4bTo6xocx5Y7mOiBe1vefUJyfT_UA8jyaxYPxkJQj1YEBOQVFBP-1z_8pl3GtU1uupwlYjy7sCvIIFK6QfH6jjAg3gPFm7PAXZ6DSN5SM_XbR1EYTeTV3BtQlEGMQiJfVVZVb4yId9lY")',
                        }}
                      />
                      <button className="px-6 py-2 border border-[#cfdbe7] rounded-lg text-[#0d141b] font-medium hover:bg-slate-50 transition-colors">
                        Change Photo
                      </button>
                    </div>
                  </div>

                  {/* Form Fields */}
                  <div className="space-y-6">
                    <div>
                      <label className="text-[#0d141b] font-medium text-sm mb-2 block">
                        Full Name
                      </label>
                      <input
                        type="text"
                        name="fullName"
                        value={formData.fullName}
                        onChange={handleFormChange}
                        className="w-full px-4 py-2 border border-[#cfdbe7] rounded-lg text-[#0d141b] focus:outline-none focus:ring-2 focus:ring-[#0d141b] bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-[#0d141b] font-medium text-sm mb-2 block">
                        Email
                      </label>
                      <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleFormChange}
                        className="w-full px-4 py-2 border border-[#cfdbe7] rounded-lg text-[#0d141b] focus:outline-none focus:ring-2 focus:ring-[#0d141b] bg-white"
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="text-[#0d141b] font-medium text-sm mb-2 block">
                          Institution
                        </label>
                        <input
                          type="text"
                          name="institution"
                          value={formData.institution}
                          onChange={handleFormChange}
                          className="w-full px-4 py-2 border border-[#cfdbe7] rounded-lg text-[#0d141b] focus:outline-none focus:ring-2 focus:ring-[#0d141b] bg-white"
                        />
                      </div>
                      <div>
                        <label className="text-[#0d141b] font-medium text-sm mb-2 block">
                          Role
                        </label>
                        <input
                          type="text"
                          name="role"
                          value={formData.role}
                          onChange={handleFormChange}
                          className="w-full px-4 py-2 border border-[#cfdbe7] rounded-lg text-[#0d141b] focus:outline-none focus:ring-2 focus:ring-[#0d141b] bg-white"
                        />
                      </div>
                    </div>
                    <div>
                      <label className="text-[#0d141b] font-medium text-sm mb-2 block">
                        Bio
                      </label>
                      <textarea
                        name="bio"
                        value={formData.bio}
                        onChange={handleFormChange}
                        rows={4}
                        className="w-full px-4 py-2 border border-[#cfdbe7] rounded-lg text-[#0d141b] focus:outline-none focus:ring-2 focus:ring-[#0d141b] bg-white resize-none"
                      />
                    </div>
                  </div>
                </div>

                <div className="flex gap-4 pt-6 border-t border-[#e7edf3]">
                  <button className="px-6 py-2 bg-[#0d141b] text-white rounded-lg font-medium hover:bg-[#0d141b]/90 transition-colors">
                    Save Changes
                  </button>
                  <button className="px-6 py-2 border border-[#cfdbe7] rounded-lg text-[#0d141b] font-medium hover:bg-slate-50 transition-colors">
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {/* Security Tab */}
            {activeTab === "security" && (
              <div className="space-y-8">
                <div>
                  <h2 className="text-[22px] font-bold text-[#0d141b] mb-6">
                    Security Settings
                  </h2>

                  {/* Change Password */}
                  <div className="pb-8 border-b border-[#e7edf3]">
                    <h3 className="text-[#0d141b] font-bold text-base mb-4">
                      Change Password
                    </h3>
                    <div className="space-y-4">
                      <div className="relative">
                        <label className="text-[#0d141b] font-medium text-sm mb-2 block">
                          Current Password
                        </label>
                        <input
                          type="password"
                          name="currentPassword"
                          value={passwordData.currentPassword}
                          onChange={handlePasswordChange}
                          className="w-full px-4 py-2 border border-[#cfdbe7] rounded-lg text-[#0d141b] focus:outline-none focus:ring-2 focus:ring-[#0d141b] bg-white"
                        />
                      </div>
                      <div className="relative">
                        <label className="text-[#0d141b] font-medium text-sm mb-2 block">
                          New Password
                        </label>
                        <div className="relative">
                          <input
                            type={showPassword ? "text" : "password"}
                            name="newPassword"
                            value={passwordData.newPassword}
                            onChange={handlePasswordChange}
                            className="w-full px-4 py-2 border border-[#cfdbe7] rounded-lg text-[#0d141b] focus:outline-none focus:ring-2 focus:ring-[#0d141b] bg-white pr-10"
                          />
                          <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="absolute right-3 top-1/2 -translate-y-1/2 text-[#4c739a]"
                          >
                            {showPassword ? (
                              <EyeOff className="w-5 h-5" />
                            ) : (
                              <Eye className="w-5 h-5" />
                            )}
                          </button>
                        </div>
                      </div>
                      <div>
                        <label className="text-[#0d141b] font-medium text-sm mb-2 block">
                          Confirm Password
                        </label>
                        <input
                          type={showPassword ? "text" : "password"}
                          name="confirmPassword"
                          value={passwordData.confirmPassword}
                          onChange={handlePasswordChange}
                          className="w-full px-4 py-2 border border-[#cfdbe7] rounded-lg text-[#0d141b] focus:outline-none focus:ring-2 focus:ring-[#0d141b] bg-white"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Two-Factor Authentication */}
                  <div className="pt-8">
                    <h3 className="text-[#0d141b] font-bold text-base mb-4">
                      Two-Factor Authentication
                    </h3>
                    <div className="p-4 bg-slate-50 rounded-lg border border-[#cfdbe7] mb-4">
                      <p className="text-[#4c739a] text-sm mb-4">
                        Add an extra layer of security to your account
                      </p>
                      <button className="px-6 py-2 border border-[#cfdbe7] rounded-lg text-[#0d141b] font-medium hover:bg-white transition-colors">
                        Enable 2FA
                      </button>
                    </div>
                  </div>
                </div>

                <div className="flex gap-4 pt-6 border-t border-[#e7edf3]">
                  <button className="px-6 py-2 bg-[#0d141b] text-white rounded-lg font-medium hover:bg-[#0d141b]/90 transition-colors">
                    Update Password
                  </button>
                  <button className="px-6 py-2 border border-[#cfdbe7] rounded-lg text-[#0d141b] font-medium hover:bg-slate-50 transition-colors">
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {/* Notifications Tab */}
            {activeTab === "notifications" && (
              <div className="space-y-8">
                <div>
                  <h2 className="text-[22px] font-bold text-[#0d141b] mb-6">
                    Notification Preferences
                  </h2>

                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 border border-[#cfdbe7] rounded-lg">
                      <div>
                        <p className="text-[#0d141b] font-medium">Email Notifications</p>
                        <p className="text-[#4c739a] text-sm">Receive email updates</p>
                      </div>
                      <button
                        onClick={() => handleNotificationChange("emailNotifications")}
                        className={`relative w-12 h-6 rounded-full transition-colors ${notifications.emailNotifications
                          ? "bg-[#0d141b]"
                          : "bg-[#cfdbe7]"
                          }`}
                      >
                        <div
                          className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${notifications.emailNotifications
                            ? "translate-x-6"
                            : "translate-x-1"
                            }`}
                        />
                      </button>
                    </div>

                    <div className="flex items-center justify-between p-4 border border-[#cfdbe7] rounded-lg">
                      <div>
                        <p className="text-[#0d141b] font-medium">Student Questions</p>
                        <p className="text-[#4c739a] text-sm">
                          Notify when students ask questions
                        </p>
                      </div>
                      <button
                        onClick={() => handleNotificationChange("studentQuestions")}
                        className={`relative w-12 h-6 rounded-full transition-colors ${notifications.studentQuestions
                          ? "bg-[#0d141b]"
                          : "bg-[#cfdbe7]"
                          }`}
                      >
                        <div
                          className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${notifications.studentQuestions
                            ? "translate-x-6"
                            : "translate-x-1"
                            }`}
                        />
                      </button>
                    </div>

                    <div className="flex items-center justify-between p-4 border border-[#cfdbe7] rounded-lg">
                      <div>
                        <p className="text-[#0d141b] font-medium">Assessment Grading</p>
                        <p className="text-[#4c739a] text-sm">
                          Notify when assessments need grading
                        </p>
                      </div>
                      <button
                        onClick={() => handleNotificationChange("assessmentGrading")}
                        className={`relative w-12 h-6 rounded-full transition-colors ${notifications.assessmentGrading
                          ? "bg-[#0d141b]"
                          : "bg-[#cfdbe7]"
                          }`}
                      >
                        <div
                          className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${notifications.assessmentGrading
                            ? "translate-x-6"
                            : "translate-x-1"
                            }`}
                        />
                      </button>
                    </div>

                    <div className="flex items-center justify-between p-4 border border-[#cfdbe7] rounded-lg">
                      <div>
                        <p className="text-[#0d141b] font-medium">Weekly Digest</p>
                        <p className="text-[#4c739a] text-sm">
                          Receive weekly summary emails
                        </p>
                      </div>
                      <button
                        onClick={() => handleNotificationChange("weeklyDigest")}
                        className={`relative w-12 h-6 rounded-full transition-colors ${notifications.weeklyDigest
                          ? "bg-[#0d141b]"
                          : "bg-[#cfdbe7]"
                          }`}
                      >
                        <div
                          className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${notifications.weeklyDigest
                            ? "translate-x-6"
                            : "translate-x-1"
                            }`}
                        />
                      </button>
                    </div>

                    <div className="flex items-center justify-between p-4 border border-[#cfdbe7] rounded-lg">
                      <div>
                        <p className="text-[#0d141b] font-medium">System Updates</p>
                        <p className="text-[#4c739a] text-sm">
                          Get notified about system updates
                        </p>
                      </div>
                      <button
                        onClick={() => handleNotificationChange("systemUpdates")}
                        className={`relative w-12 h-6 rounded-full transition-colors ${notifications.systemUpdates
                          ? "bg-[#0d141b]"
                          : "bg-[#cfdbe7]"
                          }`}
                      >
                        <div
                          className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${notifications.systemUpdates
                            ? "translate-x-6"
                            : "translate-x-1"
                            }`}
                        />
                      </button>
                    </div>
                  </div>
                </div>

                <div className="flex gap-4 pt-6 border-t border-[#e7edf3]">
                  <button className="px-6 py-2 bg-[#0d141b] text-white rounded-lg font-medium hover:bg-[#0d141b]/90 transition-colors">
                    Save Preferences
                  </button>
                </div>
              </div>
            )}

            {/* Preferences Tab */}
            {activeTab === "preferences" && (
              <div className="space-y-8">
                <div>
                  <h2 className="text-[22px] font-bold text-[#0d141b] mb-6">
                    Preferences
                  </h2>

                  <div className="space-y-6">
                    <div>
                      <label className="text-[#0d141b] font-medium text-sm mb-2 block">
                        Theme
                      </label>
                      <select
                        value={preferences.theme}
                        onChange={(e) =>
                          setPreferences((prev) => ({
                            ...prev,
                            theme: e.target.value,
                          }))
                        }
                        className="w-full px-4 py-2 border border-[#cfdbe7] rounded-lg text-[#0d141b] focus:outline-none focus:ring-2 focus:ring-[#0d141b] bg-white"
                      >
                        <option value="light">Light</option>
                        <option value="dark">Dark</option>
                        <option value="auto">Auto</option>
                      </select>
                    </div>

                    <div>
                      <label className="text-[#0d141b] font-medium text-sm mb-2 block">
                        Language
                      </label>
                      <select
                        value={preferences.language}
                        onChange={(e) =>
                          setPreferences((prev) => ({
                            ...prev,
                            language: e.target.value,
                          }))
                        }
                        className="w-full px-4 py-2 border border-[#cfdbe7] rounded-lg text-[#0d141b] focus:outline-none focus:ring-2 focus:ring-[#0d141b] bg-white"
                      >
                        <option value="English">English</option>
                        <option value="Spanish">Spanish</option>
                        <option value="French">French</option>
                        <option value="German">German</option>
                      </select>
                    </div>

                    <div>
                      <label className="text-[#0d141b] font-medium text-sm mb-2 block">
                        Default View
                      </label>
                      <select
                        value={preferences.defaultView}
                        onChange={(e) =>
                          setPreferences((prev) => ({
                            ...prev,
                            defaultView: e.target.value,
                          }))
                        }
                        className="w-full px-4 py-2 border border-[#cfdbe7] rounded-lg text-[#0d141b] focus:outline-none focus:ring-2 focus:ring-[#0d141b] bg-white"
                      >
                        <option value="dashboard">Dashboard</option>
                        <option value="analytics">Analytics</option>
                        <option value="features">Features</option>
                      </select>
                    </div>

                    <div className="flex items-center justify-between p-4 border border-[#cfdbe7] rounded-lg">
                      <div>
                        <p className="text-[#0d141b] font-medium">Auto-Save</p>
                        <p className="text-[#4c739a] text-sm">
                          Automatically save changes
                        </p>
                      </div>
                      <button
                        onClick={() =>
                          setPreferences((prev) => ({
                            ...prev,
                            autoSave: !prev.autoSave,
                          }))
                        }
                        className={`relative w-12 h-6 rounded-full transition-colors ${preferences.autoSave
                          ? "bg-[#0d141b]"
                          : "bg-[#cfdbe7]"
                          }`}
                      >
                        <div
                          className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${preferences.autoSave
                            ? "translate-x-6"
                            : "translate-x-1"
                            }`}
                        />
                      </button>
                    </div>
                  </div>
                </div>

                <div className="flex gap-4 pt-6 border-t border-[#e7edf3]">
                  <button className="px-6 py-2 bg-[#0d141b] text-white rounded-lg font-medium hover:bg-[#0d141b]/90 transition-colors">
                    Save Preferences
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
