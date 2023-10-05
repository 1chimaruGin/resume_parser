<template>
  <div style="width: 80vw; margin: auto; padding: 40px 0px">
    <v-row justify="center" align="center" style="margin: 10px 0 20px 0">
      <v-col style="text-align: center">
        <h1 style="font-weight: 600;">Choose your plan</h1>
        <h2>Boost your interview chances. Cancel any time.</h2>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="8" md="4" lg="4" xl="4" xxl="4" style="margin: 36px 0;">
        <div class="free">
          <div style="height: 90px; text-align: center">
            <h3 class="mb-3" style="font-weight: 600">Free</h3>
            <p style="white-space: nowrap">$0 every month</p>
          </div>
          <v-btn variant="outlined" width="100%" class="my-10" color="var(--orange-color)"
            >Select</v-btn
          >
          <div>
            <div style="display: flex; align-items: center">
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>5 Match Rate calculations / month</span>
            </div>
            <div style="display: flex; align-items: center">
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>5 Keyword Comparisons / month</span>
            </div>
            <div style="display: flex; align-items: center">
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Limited Scan History</span>
            </div>
            <div style="display: flex; align-items: center">
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Resume Manager</span>
            </div>
            <div style="display: flex; align-items: center">
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Jobscan Learning Center</span>
            </div>
          </div>
        </div>
      </v-col>
      <v-col cols="8" md="4" lg="4" xl="4" xxl="4">
        <div
          style="
            border: 1px solid var(--orange-color);
            border-radius: 5px;
            background: var(--orange-color);
            color: white;
            text-align: center;
            line-height: 35px;
          "
        >
          Most Popular
        </div>
        <div class="free">
          <div style="height: 90px; text-align: center">
            <h3 class="mb-3" style="font-weight: 600">2 Weeks Free</h3>
            <p>$89.95 every 3 month after FREE trial</p>
            <p style="color: var(--orange-color)">Save 40%</p>
          </div>
          <v-btn
            variant="outlined"
            width="100%"
            class="my-10"
            color="var(--blue-color)"
            style="text-transform: capitalize; background-color: var(--orange-color); color: white"
            >Try For Free</v-btn
          >
          <div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Unlimited Match Rate calculations</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Unlimited Keyword Comparisons</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Unlimited Scan History</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>LinkedIn Optimization (after trial)</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Cover Letter Optimization</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Resume Power Edit</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Job Tracker</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Predicted Skills</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Resume Manager</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Jobscan Learning Center</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Jobs Matcher</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Premium ATS &amp; Recruiter Findings</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>ATS Revealed eBook</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>ATS Friendly Resume Templates</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Premium Cover Letter Template</span>
            </div>
          </div>
        </div>
      </v-col>
      <v-col cols="8" md="4" lg="4" xl="4" xxl="4" style="margin-top: 36px;">
        <div class="free">
          <div style="height: 90px; text-align: center">
            <h3 class="mb-3" style="font-weight: 600">Monthly</h3>
            <p style="white-space: nowrap">$49.95 every month</p>
            <p style="color: var(--orange-color)">Save 0%</p>
          </div>
          <v-btn variant="outlined" width="100%" class="my-10" color="var(--orange-color)"
            >Select</v-btn
          >
          <div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Unlimited Match Rate calculations</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Unlimited Keyword Comparisons</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Unlimited Scan History</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>LinkedIn Optimization</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Cover Letter Optimization</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Resume Power Edit</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Job Tracker</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Predicted Skills</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Resume Manager</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Jobscan Learning Center</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Jobs Matcher</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Premium ATS &amp; Recruiter Findings</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>ATS Revealed eBook</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>ATS Friendly Resume Templates</span>
            </div>
            <div>
              <v-icon icon="fab fa-check" size="15" class="me-2" color="var(--orange-color)" />
              <span>Premium Cover Letter Template</span>
            </div>
          </div>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Price extends Vue {
}
</script>

<style scoped>
.free {
  border: 1px solid var(--orange-color);
  padding: 20px;
  width: 100%;
  height: max-content;
  margin: auto;
  justify-content: center;
  border-radius: 5px;
}
</style>
