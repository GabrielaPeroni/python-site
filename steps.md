# MaricaCity - Development Steps

This document outlines the detailed development steps for building the MaricaCity tourism platform.

---

## 📋 Overview

**Total Tasks:** 20
**Current Phase:** Phase 2 - Database Models
**Status:** In Progress

---

## Phase 1: Infrastructure & Setup

### Task 1: Set up PostgreSQL database configuration

**Status:** ✅ Completed

**Description:**
Configure Django to use PostgreSQL instead of SQLite for production-ready database management.

**Steps:**

1. Install `psycopg2-binary` package via Poetry
2. Update `config/settings.py` with PostgreSQL database configuration
3. Set up environment variables for database credentials
4. Install and configure PostgreSQL locally (or use Docker)
5. Create database and test connection
6. Update Makefile with database setup commands

**Dependencies:**

- PostgreSQL installed on system
- Environment variable management (python-decouple or django-environ)

**Files to modify:**

- `pyproject.toml` (add dependencies)
- `config/settings.py` (database configuration)
- `.env.example` (template for environment variables)
- `Makefile` (add database commands)

---

### Task 2: Install and configure Tailwind CSS for Django

**Status:** ✅ Completed

**Description:**
Integrate Tailwind CSS with Django for modern, utility-first styling and responsive design.

**Steps:**

1. Install `django-tailwind` package via Poetry
2. Create a theme app using Tailwind
3. Configure Tailwind in Django settings
4. Set up npm/node for Tailwind compilation
5. Configure static files settings
6. Create base template with Tailwind CDN or compiled CSS
7. Test Tailwind classes are working

**Dependencies:**

- Node.js and npm installed
- `django-tailwind` or manual Tailwind setup

**Files to create:**

- `theme/` app directory
- `templates/base.html`
- `tailwind.config.js`

**Files to modify:**

- `config/settings.py` (add theme app, static files config)
- `pyproject.toml` (add django-tailwind)

---

## Phase 2: Database Models

### Task 3: Create custom User model with three user types

**Status:** ✅ Completed

**Description:**
Implement a custom User model that supports three distinct user types: explore-users, creation-users, and admin-users.

**Steps:**

1. Create `accounts` Django app
2. Create custom User model extending AbstractUser
3. Add `user_type` field with choices (EXPLORE, CREATION, ADMIN)
4. Add additional fields (profile picture, bio, etc.)
5. Configure AUTH_USER_MODEL in settings
6. Create and run migrations
7. Update Django admin to use custom User model
8. Create user manager for custom User model

**User Types:**

- **Explore Users:** Can browse and view places
- **Creation Users:** Can create and edit their own places
- **Admin Users:** Full access including moderation and user management

**Files to create:**

- `accounts/` app directory
- `accounts/models.py` (User model)
- `accounts/admin.py` (admin configuration)
- `accounts/managers.py` (custom user manager)

**Files to modify:**

- `config/settings.py` (AUTH_USER_MODEL setting)

---

### Task 4: Create Place model

**Status:** ✅ Completed

**Description:**
Create the core Place model to store information about tourism locations.

**Steps:**

1. Create `places` Django app
2. Create Place model with fields:
   - name (CharField)
   - description (TextField)
   - address (TextField)
   - contact_phone (CharField)
   - contact_email (EmailField)
   - contact_website (URLField)
   - created_by (ForeignKey to User)
   - created_at (DateTimeField)
   - updated_at (DateTimeField)
   - is_approved (BooleanField)
   - is_active (BooleanField)
   - latitude (DecimalField, optional)
   - longitude (DecimalField, optional)
3. Add `__str__` method
4. Add Meta class with ordering
5. Create and run migrations
6. Register model in Django admin

**Files to create:**

- `places/` app directory
- `places/models.py`
- `places/admin.py`

**Files to modify:**

- `config/settings.py` (add places app)

---

### Task 5: Create Category model and relationships

**Status:** ✅ Completed

**Description:**
Create Category model for organizing places (restaurants, arts, culture, etc.) and establish relationships.

**Steps:**

1. Create Category model in places app:
   - name (CharField)
   - slug (SlugField)
   - description (TextField)
   - icon (CharField or ImageField)
   - order (IntegerField for sorting)
2. Add ManyToMany relationship between Place and Category
3. Add helper methods (get_places_count, etc.)
4. Create and run migrations
5. Register Category in Django admin
6. Create initial categories via data migration or admin

**Suggested Categories:**

- Restaurants
- Arts & Culture
- Nature & Parks
- Hotels & Accommodation
- Shopping
- Entertainment
- Historical Sites

**Files to modify:**

- `places/models.py` (add Category model)
- `places/admin.py` (register Category)

---

### Task 6: Create PlaceApproval model for moderation

**Status:** ✅ Completed

**Description:**
Implement a moderation system where creation-users submit places for admin approval.

**Steps:**

1. Create PlaceApproval model:
   - place (OneToOneField to Place)
   - submitted_by (ForeignKey to User)
   - submitted_at (DateTimeField)
   - reviewed_by (ForeignKey to User, nullable)
   - reviewed_at (DateTimeField, nullable)
   - status (CharField with choices: PENDING, APPROVED, REJECTED)
   - rejection_reason (TextField, nullable)
2. Add signals to auto-create PlaceApproval when Place is created
3. Create helper methods (approve, reject, etc.)
4. Create and run migrations
5. Register in Django admin with custom actions

**Approval Workflow:**

1. Creation-user creates Place (is_approved=False)
2. PlaceApproval record created automatically
3. Admin reviews in approval page
4. Admin approves/rejects
5. Place is_approved updated accordingly

**Files to modify:**

- `places/models.py` (add PlaceApproval model)
- `places/signals.py` (create approval on place creation)
- `places/admin.py` (register with actions)

---

### Task 7: Set up media file handling for uploaded images

**Status:** ✅ Completed

**Description:**
Configure Django to handle uploaded images for places with proper storage and optimization.

**Steps:**

1. Install Pillow for image handling
2. Configure MEDIA_URL and MEDIA_ROOT in settings
3. Add media URL patterns for development
4. Create PlaceImage model:
   - place (ForeignKey to Place)
   - image (ImageField)
   - caption (CharField, optional)
   - order (IntegerField for sorting)
   - is_primary (BooleanField)
   - uploaded_at (DateTimeField)
5. Consider using django-imagekit for thumbnails
6. Update .gitignore to exclude media files
7. Create and run migrations

**Files to create:**

- `places/models.py` (add PlaceImage model)
- `media/` directory

**Files to modify:**

- `config/settings.py` (MEDIA_URL, MEDIA_ROOT)
- `config/urls.py` (add media URL patterns)
- `pyproject.toml` (add Pillow, optional django-imagekit)
- `.gitignore` (exclude /media)

---

## Phase 3: Authentication System

### Task 8: Create authentication system (login/register pages)

**Status:** ✅ Completed

**Description:**
Build complete authentication system with login, registration, and user type selection.

**Steps:**

1. Create views for:
   - Login
   - Registration (with user type selection)
   - Logout
   - Password reset (optional)
2. Create forms:
   - LoginForm
   - RegistrationForm (with user_type field)
3. Create templates:
   - `login.html`
   - `register.html`
   - `password_reset.html` (optional)
4. Configure URL patterns
5. Add authentication middleware checks
6. Style forms with Tailwind CSS
7. Add form validation and error messages
8. Add redirect logic based on user type

**User Registration Flow:**

1. User selects account type (explore/creation)
2. User fills registration form
3. Account created and auto-login
4. Redirect based on user type

**Files to create:**

- `accounts/views.py` (auth views)
- `accounts/forms.py` (auth forms)
- `accounts/urls.py`
- `templates/accounts/login.html`
- `templates/accounts/register.html`

**Files to modify:**

- `config/urls.py` (include accounts URLs)
- `config/settings.py` (LOGIN_URL, LOGIN_REDIRECT_URL)

---

## Phase 4: User-Facing Pages

### Task 9: Build landing page with place previews

**Status:** ✅ Completed

**Description:**
Create an attractive landing page showcasing featured places and providing site navigation.

**Steps:**

1. Create home view and URL pattern
2. Create landing page template with sections:
   - Hero section with site description
   - Featured/newly added places (3-6 cards)
   - Categories overview with icons
   - Login/Register button in navigation
   - Footer with links
3. Query approved places for display
4. Style with Tailwind CSS (responsive design)
5. Add animations/transitions (optional)
6. Optimize images for fast loading

**Page Components:**

- Navigation bar with logo and login button
- Hero banner
- Place preview cards (image, name, category)
- Category tiles
- Footer

**Files to create:**

- `places/views.py` (home view)
- `templates/places/landing.html`
- `places/urls.py`

**Files to modify:**

- `config/urls.py` (set root URL)

---

### Task 10: Build explore page with categories and spotlights

**Status:** ✅ Completed

**Description:**
Create an explore page displaying all categories with featured/trending places.

**Steps:**

1. Create explore view
2. Query all categories with place counts
3. Get spotlight places (newly added, trending)
4. Create template with:
   - Category cards/buttons
   - Newly added places section
   - Trending places section (based on views/date)
   - Search bar (optional for future)
5. Style with Tailwind grid layout
6. Add filters/sorting options
7. Implement pagination if needed

**Spotlight Criteria:**

- Newly Added: Places approved in last 7 days
- Trending: Most viewed or most recent

**Files to create:**

- `templates/places/explore.html`

**Files to modify:**

- `places/views.py` (add explore view)
- `places/urls.py` (add explore URL)

---

### Task 11: Build category listing page with place previews

**Status:** ⏳ Pending

**Description:**
Create a page displaying all places within a specific category.

**Steps:**

1. Create category detail view (filtered by category slug)
2. Query all approved places in category
3. Create template with:
   - Category header (name, description, icon)
   - Grid of place cards (large, descriptive)
   - Each card shows: image, name, short description, creator
   - Link to place detail page
   - Link back to creator profile (optional)
4. Implement pagination
5. Add sorting options (newest, name, etc.)
6. Style with Tailwind

**Place Card Components:**

- Primary image
- Place name
- Short description (truncated)
- Category badges
- "View Details" button
- Creator attribution

**Files to create:**

- `templates/places/category_detail.html`

**Files to modify:**

- `places/views.py` (add category view)
- `places/urls.py` (add category URL with slug)

---

### Task 12: Build individual place detail page

**Status:** ⏳ Pending

**Description:**
Create detailed page showing all information about a specific place.

**Steps:**

1. Create place detail view
2. Query place with all related data (images, category)
3. Create template with:
   - Image gallery/carousel
   - Place name and description
   - Category badges
   - Contact information (phone, email, website)
   - Location/map (if coordinates available)
   - Creator information
   - Edit button (only for creator or admin)
   - Back to category button
4. Implement image lightbox/modal
5. Add social sharing buttons (optional)
6. Style with Tailwind
7. Track page views for trending calculation (optional)

**Page Sections:**

- Image gallery
- Main info (name, description)
- Contact details card
- Map section (if coordinates exist)
- Related places (same category)

**Files to create:**

- `templates/places/place_detail.html`

**Files to modify:**

- `places/views.py` (add detail view)
- `places/urls.py` (add place detail URL)

---

## Phase 5: Creation Features

### Task 13: Build place creation page for creation-users

**Status:** ⏳ Pending

**Description:**
Create interface for creation-users to submit new places for approval.

**Steps:**

1. Create PlaceCreateView (LoginRequired, UserType check)
2. Create PlaceForm with all fields
3. Create PlaceImageFormSet for multiple images
4. Create template with:
   - Form fields (name, description, contact info)
   - Category selection (multiple)
   - Image upload (multiple files)
   - Primary image selector
   - Preview section (optional)
   - Submit for approval button
5. Add form validation
6. On submit: create Place (is_approved=False) + images
7. Show success message and redirect
8. Send notification to admins (optional)
9. Style with Tailwind

**Permissions:**

- Only creation-users and admin-users can access
- Places start as unapproved

**Files to create:**

- `templates/places/place_form.html`

**Files to modify:**

- `places/views.py` (add create view)
- `places/forms.py` (create forms)
- `places/urls.py` (add create URL)

---

### Task 14: Build place edit functionality for creation-users

**Status:** ⏳ Pending

**Description:**
Allow creation-users to edit their own places and admins to edit any place.

**Steps:**

1. Create PlaceUpdateView with permissions check
2. Reuse PlaceForm from creation
3. Allow editing of images (add/remove/reorder)
4. Create template (similar to creation page)
5. Add permission checks:
   - Creator can edit their own places
   - Admins can edit any place
6. If place was approved and edited, set to pending again (optional)
7. Show edit history (optional)
8. Add delete functionality with confirmation
9. Style with Tailwind

**Permission Rules:**

- Creator: Edit only own places
- Admin: Edit any place
- Explore users: Cannot edit

**Files to create:**

- `templates/places/place_update.html`
- `templates/places/place_delete_confirm.html`

**Files to modify:**

- `places/views.py` (add update/delete views)
- `places/urls.py` (add edit/delete URLs)

---

## Phase 6: Admin Features

### Task 15: Build admin approval page with pending entries

**Status:** ⏳ Pending

**Description:**
Create dashboard for admin-users to review and approve/reject pending places.

**Steps:**

1. Create ApprovalListView (admin only)
2. Query all places with status PENDING
3. Create template with:
   - Table/cards of pending places
   - Place preview (image, name, description)
   - Creator information
   - Approve/Reject buttons
   - Quick view modal
4. Create approval action view
5. Create rejection view with reason form
6. Update PlaceApproval status accordingly
7. Send notification to creator (optional)
8. Style with Tailwind
9. Add bulk actions (approve multiple)

**Approval Actions:**

- Approve: Set is_approved=True, update status
- Reject: Set status=REJECTED, save reason
- View Details: Open full place detail

**Files to create:**

- `templates/admin_panel/approval_list.html`
- `templates/admin_panel/rejection_form.html`

**Files to modify:**

- `places/views.py` (add admin views)
- `places/urls.py` (add admin URLs)

---

### Task 16: Build admin backlog view for all entries history

**Status:** ⏳ Pending

**Description:**
Create comprehensive view of all places regardless of approval status for audit purposes.

**Steps:**

1. Create BacklogListView (admin only)
2. Query ALL places with all statuses
3. Create template with:
   - Filterable table (by status, date, creator)
   - Search functionality
   - Columns: name, creator, status, submitted date, reviewed date
   - Actions: view, edit, delete
   - Export to CSV (optional)
4. Implement filters and search
5. Add pagination
6. Show approval history
7. Style with Tailwind

**Filter Options:**

- Status: All, Pending, Approved, Rejected
- Date range: submitted, reviewed
- Creator: specific user
- Category: specific category

**Files to create:**

- `templates/admin_panel/backlog_list.html`

**Files to modify:**

- `places/views.py` (add backlog view)
- `places/urls.py` (add backlog URL)

---

### Task 17: Implement admin user management

**Status:** ⏳ Pending

**Description:**
Create interface for admins to manage user accounts, permissions, and status.

**Steps:**

1. Create UserManagementView (admin only)
2. List all users with details
3. Create template with:
   - User table (username, email, type, status, date joined)
   - Change user type dropdown
   - Activate/deactivate toggle
   - Delete user button
   - User detail/edit modal
4. Create user edit form
5. Add permission change functionality
6. Add account status toggle (active/inactive)
7. Add user deletion with confirmation
8. Show user statistics (places created, etc.)
9. Style with Tailwind

**Admin Capabilities:**

- Change user type (explore ↔ creation)
- Activate/deactivate accounts
- Delete users (with cascade considerations)
- View user activity/statistics

**Files to create:**

- `templates/admin_panel/user_management.html`
- `templates/admin_panel/user_detail.html`

**Files to modify:**

- `accounts/views.py` (add management views)
- `accounts/urls.py` (add management URLs)

---

## Phase 7: Security & Polish

### Task 18: Add permission checks and access control

**Status:** ⏳ Pending

**Description:**
Implement comprehensive permission system throughout the site.

**Steps:**

1. Create permission decorators/mixins:
   - `@creation_user_required`
   - `@admin_user_required`
   - `LoginRequiredMixin` for class views
2. Create permission checker utilities
3. Add checks to all views:
   - Place creation: creation/admin only
   - Place edit: owner or admin only
   - Approval pages: admin only
   - User management: admin only
4. Add template conditionals for buttons/links
5. Test all permission scenarios
6. Add proper 403 error page
7. Add permission tests

**Permission Matrix:**
| Feature | Explore User | Creation User | Admin User |
|---------|--------------|---------------|------------|
| View Places | ✅ | ✅ | ✅ |
| Create Places | ❌ | ✅ | ✅ |
| Edit Own Places | ❌ | ✅ | ✅ |
| Edit Any Place | ❌ | ❌ | ✅ |
| Approve Places | ❌ | ❌ | ✅ |
| User Management | ❌ | ❌ | ✅ |

**Files to create:**

- `accounts/decorators.py`
- `accounts/mixins.py`
- `templates/403.html`

**Files to modify:**

- All view files (add permission checks)
- All templates (add conditionals)

---

### Task 19: Style all pages with Tailwind CSS for responsive design

**Status:** ⏳ Pending

**Description:**
Ensure all pages are fully styled, responsive, and follow consistent design patterns.

**Steps:**

1. Create design system/style guide:
   - Color palette
   - Typography scale
   - Spacing system
   - Component patterns
2. Style all templates:
   - Navigation (mobile + desktop)
   - Forms (consistent styling)
   - Buttons (primary, secondary, danger)
   - Cards (place cards, category cards)
   - Tables (admin views)
   - Modals/dialogs
3. Implement responsive breakpoints:
   - Mobile (sm)
   - Tablet (md)
   - Desktop (lg, xl)
4. Add loading states
5. Add empty states
6. Add error states
7. Test on multiple screen sizes
8. Optimize for accessibility (ARIA labels, contrast)

**Components to Style:**

- Navigation bar
- Footer
- Hero sections
- Place cards
- Form inputs
- Buttons
- Modals
- Tables
- Pagination
- Flash messages/alerts

**Files to modify:**

- All template files
- `templates/base.html`
- Tailwind config

---

### Task 20: Test complete user workflows for all three user types

**Status:** ⏳ Pending

**Description:**
Comprehensive testing of all user journeys and functionality.

**Steps:**

1. Create test scenarios for each user type
2. Test explore-user workflow:
   - View landing page
   - Browse categories
   - View place details
   - Register account
3. Test creation-user workflow:
   - Register as creation-user
   - Create new place
   - Upload images
   - Submit for approval
   - Edit own place
   - View approval status
4. Test admin-user workflow:
   - Access approval queue
   - Approve/reject places
   - View backlog
   - Manage users
   - Edit any place
5. Test edge cases:
   - Permission violations
   - Invalid form data
   - Empty states
   - Large image uploads
6. Test responsive design on devices
7. Write automated tests (unit + integration)
8. Fix any bugs found
9. Performance testing
10. Security testing

**Test Checklist:**

- [ ] User registration/login works
- [ ] All user types have correct permissions
- [ ] Place creation/edit works
- [ ] Image upload works
- [ ] Approval workflow complete
- [ ] Admin can manage users
- [ ] All pages are responsive
- [ ] Forms validate correctly
- [ ] Error messages display properly
- [ ] Performance is acceptable

**Files to create:**

- `accounts/tests.py`
- `places/tests.py`
- Test data fixtures

---

## 🔄 Progress Tracking

**Legend:**

- ⏳ Pending
- 🔄 In Progress
- ✅ Completed
- ⚠️ Blocked

**Current Status:**

- Phase 1: ✅ Completed (2/2 tasks)
- Phase 2: ✅ Completed (5/5 tasks)
- Phase 3: ✅ Completed (1/1 tasks)
- Phase 4: 🔄 In Progress (2/4 tasks)
- Phase 5: ⏳ Not Started (0/2 tasks)
- Phase 6: ⏳ Not Started (0/3 tasks)
- Phase 7: ⏳ Not Started (0/2 tasks)

**Overall Progress:** 10/20 tasks completed (50%)

---

## 📝 Notes

- Update this file as you complete tasks
- Mark tasks in progress with 🔄
- Mark completed tasks with ✅
- Add any blockers or notes under relevant tasks
- Keep the progress tracking section updated

---

## 🚀 Next Steps

1. Begin with Task 1: PostgreSQL setup
2. Then proceed to Task 2: Tailwind CSS
3. Continue in sequential order unless dependencies require different order

Ready to start building! 🎉
