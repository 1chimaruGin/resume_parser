<template>
  <div class="container">
    <Nav />
    <v-row class="row1" justify="center" align="center">
      <v-col cols="12" sm="6" md="6" lg="6" xl="6" xxl="6" align="center">
        <div class="row1col1">
          <h1>
            land more interviews with an optimized resume.
            <br />
            <span style="border-bottom: 2px var(--red-color) dashed; border">Start For Free.</span>
          </h1>
          <p style="font-weight: 400; font-size: 25px; line-height: 130%; color: #f7f7ee">
            {{ resumes }} resumes scanned.
          </p>
        </div>
      </v-col>
      <v-col cols="6" class="header-image" align="center">
        <div class="row1col2">
          <img alt="resume" src="@/assets/images/res.svg" style="width: 30vw" />
        </div>
      </v-col>
      <v-col cols="12" class="pt-0">
        <p style="color: #f7f7ee; font-size: 18px">Get Started Below</p>
        <v-icon icon="fab fa-angle-down" color="#F7F7EE" size="50" />
      </v-col>
    </v-row>
    <v-row no-gutters justify="center" class="pa-8">
      <p class="steps">3 steps to score</p>
    </v-row>
    <!-- steps -->
    <v-row justify="center" class="pb-8 px-8 px-lg-0 px-xl-0 px-xxl-0 custom-width">
      <v-col cols="12" sm="6" md="6" lg="4" xl="4" xxl="4">
        <div>
          <div class="step-block">
            <span>Step 1</span>
            <p>Copy/paste or upload your resume here:</p>
          </div>
          <div class="step-box">
            <div>
              <!-- <p>Click here to paste text</p>
              <p>or</p> -->
              <p>Upload a PDF, PNG, or JPG File</p>
              <br />
              <v-file-input
                show-size
                color="var(--blue-color)"
                label="Upload Resume"
                prepend-icon="mdi:mdi-paperclip"
                style="color: var(--blue-color)"
              >
              </v-file-input>
              <!-- <v-btn color="var(--blue-color)" class="text-white mt-5">Upload Resume</v-btn> -->
            </div>
          </div>
        </div>
      </v-col>
      <v-col cols="12" sm="6" md="6" lg="4" xl="4" xxl="4">
        <div>
          <div class="step-block">
            <span>Step 2</span>
            <p>Paste the job post's details here:</p>
          </div>
          <div class="step-box">
            <v-form>
              <div>
                <label style="text-align: start; display: block">Job Title</label>
                <input v-model="jobTitle" name="jobTitle" class="custom-input" type="text" />
              </div>
              <div>
                <label style="text-align: start" class="d-block">Industry</label>
                <input v-model="industry" name="industry" class="custom-input" type="text" />
              </div>
              <div>
                <label style="text-align: start" class="d-block">Job Description</label>
                <textarea
                  v-model="jobDescription"
                  name="jobDescription"
                  class="custom-textarea"
                  type="textarea"
                ></textarea>
              </div>
            </v-form>
          </div>
        </div>
      </v-col>
      <v-col cols="12" sm="6" md="6" lg="4" xl="4" xxl="4">
        <div>
          <div class="step-block">
            <span>Step 3</span>
            <p>Scan to compare and score your resume vs the job's description.</p>
          </div>
          <div class="pa-5">
            <div class="" style="text-align: end">
              <img alt="arrow image" src="@/assets/images/down-arrow-top.png" />
            </div>
            <div class="">
              <v-btn color="var(--red-color)" class="text-white mt-5 px-10" style="font-weight: 700"
                >Start Resume Scan ></v-btn
              >
              <!-- <p style="color: var(--blue-color);">Or see a sample resume scan ></p> -->
            </div>
          </div>
        </div>
      </v-col>
    </v-row>
    <!-- current situation text -->
    <v-row
      no-gutters
      justify="center"
      align="center"
      class="py-8 px-8 px-lg-0 px-xl-0 px-xxl-0 custom-width"
    >
      <v-col
        cols="12"
        xs="6"
        sm="6"
        md="6"
        lg="6"
        xl="6"
        xxl="6"
        class="mb-6 mb-sm-0 mb-md-0 mb-lg-0 mb-xl-0 mb-xxl-0"
      >
        <img
          alt="resume"
          src="@/assets/images/interviews2.png"
          style="max-width: 490px; width: 100%; padding-right: 25px"
        />
      </v-col>
      <v-col cols="12" sm="6" md="6" lg="6" xl="6" xxl="6">
        <h2
          style="
            text-transform: uppercase;
            text-align: left;
            font-weight: 800;
            font-size: 17px;
            line-height: 130%;
            margin-bottom: 24px;
          "
        >
          Why Does Resymatch Work?
        </h2>
        <h3
          style="
            font-weight: 700;
            font-size: 40px;
            text-align: left;
            line-height: 130%;
            margin-bottom: 24px;
          "
        >
          Only <span style="color: var(--red-color)">2%</span> Of Resumes Land Interviews.
        </h3>
        <div class="paragraph">
          <p>
            Want to be one of them? Optimize your resume with the right ATS keywords, formatting,
            and best practices. See how with our resume sanner.
          </p>
          <p>ResyMatch helps you optimize your resume to become part of the 2%.</p>
        </div>
        <v-row justify="center" class="mt-5 d-none d-lg-flex">
          <v-col cols="4">
            <div style="text-align: center">
              <img src="@/assets/images/250-resumes.png" alt="250 resume" width="80" height="80" />
              <strong class="strong-text">250</strong>
              <p>resumes will be submitted for the average open role.</p>
            </div>
          </v-col>
          <v-col cols="4">
            <div style="text-align: center">
              <img src="@/assets/images/5-interview.png" alt="250 resume" width="80" height="80" />
              <strong class="strong-text">~5</strong>
              <p>of the candidates will be interviewed.</p>
            </div>
          </v-col>
          <v-col cols="4">
            <div style="text-align: center">
              <img src="@/assets/images/1-job-offer.png" alt="250 resume" width="80" height="80" />
              <strong class="strong-text">1</strong>
              <p>will get a job offer.</p>
            </div>
          </v-col>
        </v-row>
      </v-col>
      <v-col class="d-block d-lg-none px-3">
        <v-row justify="center" class="mt-5">
          <v-col cols="4">
            <div style="text-align: center">
              <img src="@/assets/images/250-resumes.png" alt="250-resume" width="80" height="80" />
              <strong class="strong-text">250</strong>
              <p>resumes will be submitted for the average open role.</p>
            </div>
          </v-col>
          <v-col cols="4">
            <div style="text-align: center">
              <img src="@/assets/images/5-interview.png" alt="5-interview" width="80" height="80" />
              <strong class="strong-text">~5</strong>
              <p>of the candidates will be interviewed.</p>
            </div>
          </v-col>
          <v-col cols="4">
            <div style="text-align: center">
              <img src="@/assets/images/1-job-offer.png" alt="1-job-offer" width="80" height="80" />
              <strong class="strong-text">1</strong>
              <p>will get a job offer.</p>
            </div>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <!-- history text -->
    <v-row no-gutters justify="center" class="pa-8 px-sm-8">
      <p class="history">
        Our resume scanner has helped people land jobs at the world best companies.
      </p>
    </v-row>
    <!-- social list -->
    <v-row no-gutters justify="center" class="pa-8 px-sm-8">
      <ul style="text-decoration: none">
        <li class="social">
          <a href="https://www.linkedin.com/" target="_blank" class="alink"
            ><v-icon size="30">home</v-icon></a>
        </li>
        <li class="social">
          <a href="https://www.instagram.com/" target="_blank" class="alink"
            ><v-icon size="30">home</v-icon></a>
        </li>
        <li class="social">
          <a href="https://www.facebook.com/" target="_blank" class="alink"
            ><v-icon icon="fab fa-facebook" size="30"
          /></a>
        </li>
        <li class="social">
          <a href="https://www.twitter.com/" target="_blank" class="alink"
            ><v-icon icon="fab fa-twitter" size="30"
          /></a>
        </li>
      </ul>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch } from 'vue-property-decorator';
import Nav from '@/components/Nav.vue';
import {
  mdiLinkedin,
  mdiInstagram,
  mdiFacebook,
  mdiTwitter,
} from '@mdi/js';

@Component({
  components: {
    Nav,
  },
})
export default class HomeView extends Vue {
  private mdiLinkedin = mdiLinkedin;
  private mdiInstagram = mdiInstagram;
  private mdiFacebook = mdiFacebook;
  private mdiTwitter = mdiTwitter;
  public resumesScanned = 468532;
  public jobTitle = '';
  public industry = '';
  public jobDescription = '';

  mounted() {
    setInterval(() => {
      this.resumesScanned++;
    }, 5000);
  }

  public get resumes() {
    return this.resumesScanned.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }
}
</script>


<style scoped>
.container {
  position: relative;
  /* border: 1px dotted green; */
  text-align: center;
  margin: auto;
  width: 100vw;
  margin-top: 20px;
  /* background: #cfcfcf; */
}
.row1 {
  background: var(--orange-color);
}
.row1col1 {
  /* width: 400px; */
  /* border: 1px dotted red; */
  margin: auto;
  padding: 0 30px;
  max-width: 550px;
}
.row1col1 h1 {
  font-size: 36px;
  text-transform: capitalize;
  font-weight: 700;
  line-height: 130%;
  /* color: #ffffff; */
  color: #f7f7ee;
  margin-bottom: 40px;
}
.row1col2 {
  /* width: 400px; */
  /* border: 1px dotted blue; */
}
.steps {
  border: 1px solid F7F7EE;
  border-radius: 50px;
  /* background: #5ABA5F; */
  background: #17706e;
  color: white;
  padding: 10px 20px;
  text-transform: uppercase;
  font-weight: 600;
  font-size: 18px;
  margin-top: 30px;
}
.step-box {
  border: 2px solid var(--blue-color);
  /* min-width: 350px; */
  min-height: 410px;
  margin-top: 10px;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.custom-input {
  border: 1px solid var(--blue-color);
  background: #e3f2fd;
  width: 20vw;
  height: 50px;
  padding: 5px;
  margin-top: 5px;
  margin-bottom: 13px;
}
/* @media (min-width: 768px) and (max-width: 868px) { */
@media (max-width: 599px) {
  .custom-input {
    width: 60vw;
  }
}
@media (min-width: 600px) and (max-width: 1279px) {
  .custom-input {
    width: 30vw;
  }
}
.custom-input:focus-visible {
  outline: none;
}
.custom-textarea {
  border: 1px solid var(--blue-color);
  background: #e3f2fd;
  width: 20vw;
  padding: 5px;
  height: 120px;
  margin-top: 5px;
  margin-bottom: 13px;
  /* overflow: auto; */
}
@media (max-width: 599px) {
  .custom-textarea {
    width: 60vw;
  }
}
@media (min-width: 600px) and (max-width: 1279px) {
  .custom-textarea {
    width: 30vw;
  }
}
.custom-textarea:focus-visible {
  outline: none;
}
.step-block p {
  font-weight: 600;
  font-size: 25px;
  line-height: 1.3em;
  min-height: 2.6em;
  text-align: start;
}
.step-block span {
  font-weight: 800;
  font-size: 25px;
  line-height: 130%;
  display: block;
  text-align: start;
}
.history {
  text-justify: center;
  text-transform: capitalize;
  font-size: 30px;
}
.social {
  width: 57px;
  height: 57px;
  border-radius: 50%;
  background: white;
  color: #6e6e6e;
  box-shadow: 0 6px 20px #d4d4d1;
  padding-top: 10px;
  margin-right: 10px;
}
.social:hover {
  color: #ffffff;
  background: var(--blue-color);
}
.social:hover .alink {
  color: #ffffff;
}
.alink {
  color: gray;
}
ul {
  list-style: none;
  display: flex;
}
.strong-text {
  font-weight: 700;
  display: block;
  font-size: 40px;
  line-height: 130%;
  color: var(--blue-color);
  margin-top: 8px;
  margin-bottom: 8px;
}
.paragraph p {
  font-weight: 400;
  font-size: 18px;
  line-height: 140%;
  text-align: left;
}
.custom-width {
  width: 100vw;
  margin: auto;
}
@media (min-width: 1280px) {
  .custom-width {
    width: 80vw;
    margin: auto;
  }
}
.header-image {
  display: block;
}
@media (max-width: 768px) {
  .header-image {
    display: none;
  }
}
</style>
