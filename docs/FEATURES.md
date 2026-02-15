# Features & Functionality

## User Roles
1.  **Admin/User (Head of Family)**: Can manage expenses, view reports, and add family members.
2.  **Family Member**: Can add their own expenses and view their own data.

## Core Modules

### 1. Expense Tracking
- **Add Expense**: Categorized transaction entry (Food, Travel, Bills, etc.).
- **View Transactions**: List view of all past transactions.
- **Edit/Delete**: Modify entries if mistakes were made.

### 2. Dashboard
- **Visual Reports**: Charts and graphs displaying spending habits.
- **Recent Activity**: Quick view of latest transactions.

### 3. Family Management
- **Add Member**: Register new family members to the same account group.
- **Family Expenses**: View expenses aggregated across all family members.

### 4. Reports & Analytics
- **Monthly Breakdown**: Filter expenses by month.
- **Category Analysis**: Pie chart of spending by category.
- **Filters**: Date range filtering (This Month, Last 6 Months, Custom).
- **PDF Export**: Download expense reports for offline viewing.

### 5. Reminders
- **Set Reminders**: Email notifications for bill payments or other tasks.
- **Automated Emails**: System sends an email when a reminder is triggered (integrated with Celery/Cron or triggered on creation for demo).

### 6. Authentication & Security
- **Secure Login**: Hashed password storage.
- **Password Reset**: OTP-based password reset via Email.
