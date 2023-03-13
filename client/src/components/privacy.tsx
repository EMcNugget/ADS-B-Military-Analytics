import "../scss/privacy.scss";
import Footer from "./footer";

const returnonclick = () => {
  history.back();
};

function Privacy() {
  return (
    <div>
      <div>
        <h1>Privacy Policy</h1>
        <p>
          Protecting your private information is our priority. This Statement of
          Privacy applies to www.adsbmilanalytics.com, and ADS-B Military
          Analytics and governs data collection and usage. For the purposes of
          this Privacy Policy, unless otherwise noted, all references to ADS-B
          Military Analytics include www.adsbmilanalytics.com. The ADS-B
          Military Analytics website is a Analytics for military aircraft over
          ADS-B. site. By using the ADS-B Military Analytics website, you
          consent to the data practices described in this statement.
        </p>
        <h3>Collection of your Personal Information</h3>
        <p>
          We do not collect any personal information about you unless you
          voluntarily provide it to us. However, we may gather additional
          personal or non-personal information in the future.
        </p>
        <h3>Sharing Information with Third Parties</h3>
        <p>
          ADS-B Military Analytics does not sell, rent or lease its customer
          lists to third parties.
        </p>
        <p>
          ADS-B Military Analytics may share data with trusted partners to help
          perform statistical analysis. All such third parties are prohibited
          from using your personal information except to provide these services
          to ADS-B Military Analytics, and they are required to maintain the
          confidentiality of your information.
        </p>
        <h3>Tracking User Behavior</h3>
        <p>
          ADS-B Military Analytics may keep track of the websites and pages our
          users visit within ADS-B Military Analytics, in order to determine
          what ADS-B Military Analytics services are the most popular. This data
          is used to deliver customized content whose behavior indicates that
          they are interested in a particular subject area.
        </p>
        <h3>Automatically Collected Information</h3>
        <p>
          Information about your computer hardware and software may be
          automatically collected by ADS-B Military Analytics. This information
          can include: your IP address, browser type, domain names, access times
          and referring website addresses. This information is used for the
          operation of the service, to maintain quality of the service, and to
          provide general statistics regarding use of the ADS-B Military
          Analytics website.
        </p>
        <p>
          This website contains links to other sites. Please be aware that we
          are not responsible for the content or privacy practices of such other
          sites. We encourage our users to be aware when they leave our site and
          to read the privacy statements of any other site that collects
          personally identifiable information.
        </p>
        <h3>Changes to this Statement</h3>
        <p>
          ADS-B Military Analytics reserves the right to change this Privacy
          Policy from time to time. We will notify you about significant changes
          in the way we treat personal information by placing a notice on our
          GitHub repository, by placing a prominent notice on our website,
          and/or by updating any privacy information. Your continued use of the
          website and/or Services available after such modifications will
          constitute your: (a) acknowledgment of the modified Privacy Policy;
          and (b) agreement to abide and be bound by that Policy.
        </p>
        <h3>Contact Information</h3>
        <p>
          ADS-B Military Analytics welcomes your questions or comments regarding
          this Statement of Privacy. If you believe that ADS-B Military
          Analytics has not adhered to this Statement, please contact ADS-B
          Military Analytics at:
        </p>
        <p>&nbsp;</p>
        <p>ADS-B Military Analytics</p>
        <p>Email Address:</p>
        <a
          className="link"
          href="mailto: support@adsbmilanalytics.com"
          target="_blank"
          rel="noreferrer"
        >
          support@adsbmilanalytics.com
        </a>
        <p>Effective as of March 02, 2023</p>
      </div>
      <div className="privacy_container">
        <input
          className="privacy_button"
          type="button"
          value="Return"
          onClick={returnonclick}
        />
      </div>
      <p>&nbsp;</p>
      <p>&nbsp;</p>
      <Footer />
    </div>
  );
}

export default Privacy;
